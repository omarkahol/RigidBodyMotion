import numpy as np
from time import time
from DrawingSchema import Drawing_Schema
from QuatPy import *
from ReferenceFrame import *
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
from matplotlib.animation import FuncAnimation
import pickle
import os
import sys
import csv

class Object:

    def __init__(self, mass, ref_frame=ReferenceFrame([0,0,0]), Io = np.diag([1,1,1]),name="None"):
        if Io.shape == (3,3):
            self.name = name
            self.N=ref_frame
            self.Io=Io
            self.mass=mass
            self.omega = np.array([0,0,0])
            self.v = np.array([0,0,0])
            self.__object_time__ = 0
            self.forces=[]
            self.__state__=[]
            self.solution=None
        else:
            raise ValueError('Io must be a 3x3 matrix')

    def __str__(self):
        return "False"

    def apply_w(self,w0):
        if len(w0)==3:
            self.omega=self.N.to_this_frame(w0)
            return True
        else:
            return False

    def set_io_matrix(self,Io):
        if Io.shape==(3,3):
            self.Io=Io
            return True
        else:
            return False

    def set_reference_frame(self,ref_frame):
        self.N=ref_frame

    def apply_v(self,v):
        if len(v)==3:
            self.v=v
        else:
            return False

    def apply_forces(self,forces):
        self.forces=forces

    def compute_io(self,xs,ys,zs):
        if len(xs)==len(ys) and len(ys)==len(zs):
            l=len(xs)
            m=self.mass/l
            io=[]
            print('computing io...')
            for ax1 in [self.N.e1,self.N.e2,self.N.e3]:
                I = np.array([0, 0, 0], dtype=float)
                for i in range(l):
                    p = self.N.base_quaternion.rotate([xs[i], ys[i], zs[i]])
                    I += m * np.cross(p, np.cross(ax1, p))
                for ax2 in [self.N.e1,self.N.e2,self.N.e3]:
                    io.append(I.dot(ax2))
            self.Io=np.array(io).reshape((3,3))
            return True
        else:
            return False

    def fix_new_origin(self,xs,ys,zs):
        if len(xs)==len(ys) and len(ys)==len(zs):
            l=len(xs)
            new_or=np.array([0,0,0],dtype=float)
            for px,py,pz in zip(xs,ys,zs):
                new_or = np.add(new_or,self.N.base_quaternion.rotate([px,py,pz]))
            self.N.origin = np.add(self.N.origin,new_or/l)
            return True
        else:
            return False


    def __compute_forces_torques__(self, state):
        F=np.array([0,0,0],dtype=float)
        T=np.array([0,0,0],dtype=float)
        for force in self.forces:
            if not force.fixed_origin:
                new_origin=Quaternion(state[6],state[7:10]).rotate(force.origin)
            else:
                new_origin=force.origin
            f=force.__expr__(*np.add(state[0:3],new_origin),self.__object_time__)
            F += f
            T += self.N.to_this_frame(np.cross(new_origin,f))
        return F, T

    def __compute_state__(self):
        self.__state__ = [*self.N.origin,*self.v,self.N.base_quaternion.s,*self.N.base_quaternion.v,*self.omega]

    def dtstate(self,state,t):
        F, T = self.__compute_forces_torques__(state)
        dvx,dvy,dvz = F/self.mass

        w1,w2,w3=state[10:]
        b0,b1,b2,b3=state[6:10]
        vx,vy,vz=state[3:6]

        dw1,dw2,dw3 = np.linalg.solve(self.Io, np.subtract(T,np.cross([w1,w2,w3], self.Io.dot([w1,w2,w3]))))

        dbeta = Quaternion(b0,[b1,b2,b3]).prod(Quaternion(0, [w1,w2,w3])).scale(0.5)
        return [vx,vy,vz,dvx,dvy,dvz,dbeta.s,*dbeta.v,dw1,dw2,dw3]

    def ellipsoid(self,n1,n2):
        a = 1 / sqrt(self.Io[0,0])
        b = 1 / sqrt(self.Io[1,1])
        c = 1 / sqrt(self.Io[2,2])
        u, v = np.meshgrid(np.linspace(0, np.pi, n1), np.linspace(0, 2 * np.pi, n2))
        return np.vstack([a*np.hstack(np.sin(u)*np.cos(v)),b*np.hstack(np.sin(u)*np.sin(v)),c*np.hstack(np.cos(u))])

    def Mo(self):
        return self.N.move_with_origin(np.cross(self.N.origin,self.mass*np.array(self.__state__[3:6])))+\
               self.N.move_with_origin(self.N.to_base_frame(self.Io.dot(self.__state__[10:13])))

    def step(self,dt):
        self.__state__=odeint(self.dtstate,self.__state__,[0,dt])[-1]
        Nx, Ny, Nz, vx, vy, vz, b0, b1, b2, b3, w1, w2, w3 = self.__state__
        self.N.origin=np.array([Nx,Ny,Nz],dtype=float)
        self.N.set_base_quaternion(b0,b1,b2,b3)
        self.omega = self.N.to_base_frame([w1,w2,w3])
        self.__object_time__ += dt


    def solve_model(self,t):
        self.__compute_state__()
        print('integrating solution...')
        solution = odeint(self.dtstate, self.__state__, t)

        origins = []
        quaternions = []
        omegas = []

        print('extracting values...')
        for state in solution:
            Nx, Ny, Nz, vx, vy, vz, b0, b1, b2, b3, w1, w2, w3 = state

            origins.append([Nx, Ny, Nz])
            quaternions.append(Quaternion(b0, [b1, b2, b3]))
            omegas.append([w1, w2, w3])

        self.solution=[origins,quaternions,omegas]

        return True

    def draw(self,drawing_schema=Drawing_Schema(),n1=20,n2=20,custom_obj=None, blit=True):
        self.__compute_state__()
        fig = plt.figure()
        ax = fig.add_subplot(111,projection='3d',xlim=drawing_schema.lim,ylim=drawing_schema.lim,zlim=drawing_schema.lim)
        canvas = drawing_schema.__set_canvas__(ax)
        ell = self.ellipsoid(n1,n2) if custom_obj is None else custom_obj

        def animate(i):
            self.step(drawing_schema.dt)
            e1,e2,e3,w,M,line,bd = drawing_schema.__update_canvas__(canvas,self,ell)
            return e1,e2,e3,w,M,line,bd

        t0 = time()
        animate(0)
        t1 = time()
        inte = 1000 * drawing_schema.dt - (t1 - t0)
        ani = FuncAnimation(fig, animate, frames=300, interval=inte, blit=blit)
        plt.show(ani)

    def integrate_and_draw(self,t,drawing_schema=Drawing_Schema(),n1=20,n2=20, custom_obj=None, blit=True, interval=None, draw_before=None):
        self.solve_model(t)
        origins, quaternions, omegas = self.solution
        if draw_before is None:
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d', xlim=drawing_schema.lim, ylim=drawing_schema.lim,
                                 zlim=drawing_schema.lim)
            canvas = drawing_schema.__set_canvas__(ax)
        else:
            canvas= drawing_schema.__set_canvas__(draw_before[1])
            fig=draw_before[0]
        ell=self.ellipsoid(n1,n2) if custom_obj is None else custom_obj

        def animate(i):
            e1, e2, e3, w, M, line, bd = drawing_schema.__update_canvas__(canvas, self, ell,state=[origins[i],
                quaternions[i],omegas[i]])
            return e1, e2, e3, w, line, M, bd

        if interval is None:
            ani = FuncAnimation(fig, animate, frames=len(t), interval=1000 * t.max() / len(t), blit=blit)
        else:
            ani = FuncAnimation(fig, animate, frames=len(t), interval=interval / len(t), blit=blit)
        plt.show(ani)

    def save(self, dirname):
        if self.solution is None:
            raise RuntimeError('The solution must be computed with solve_model')
        path = os.path.dirname(os.path.realpath('Object.py'))
        os.chdir(path)
        if not os.path.exists(dirname):
            path=os.path.join(path,dirname)
            os.mkdir(path)
        else:
            raise RuntimeError('Directory already exists')
        os.chdir(path)
        open('solution.csv', 'a').close()
        with open('solution.csv', 'w') as f:
            csvfile=csv.writer(f,delimiter='\n')
            csvfile.writerows(self.solution)
        return True

    def load(self):
        print('TODO LATER')



















