import matplotlib.pyplot as plt
import numpy as np

class Drawing_Schema:

    def __init__(self, draw_str="labwmf",dt=1/60,lim=(-10,10)):
        self.draw_line=False
        self.draw_axes=False
        self.draw_body=False
        self.draw_omega=False
        self.draw_m=False
        self.draw_base_frame=False

        for c in draw_str:
            if c=='l':
                self.draw_line=True
            elif c=='a':
                self.draw_axes=True
            elif c == 'b':
                self.draw_body = True
            elif c=='w':
                self.draw_omega=True
            elif c=='m':
                self.draw_m=True
            elif c=='f':
                self.draw_base_frame=True

        self.dt=dt
        self.lim=lim
        self.e1_s=('b-',3)
        self.e2_s = ('b-', 3)
        self.e3_s = ('b-', 3)
        self.w_s = ('k-', 2)
        self.m_s = ('r-', 1)
        self.bd_s = ('y', 1)
        self.line_s = ('k-', 0.5)

    def update_schemes(self,str_tag,data_schema):
        if str_tag == 'e1':
            self.e1_s=data_schema
            return True
        elif str_tag == 'e2':
            self.e2_s=data_schema
            return True
        elif str_tag == 'e3':
            self.e3_s=data_schema
            return True
        elif str_tag == 'w':
            self.w_s=data_schema
            return True
        elif str_tag == 'm':
            self.m_s=data_schema
            return True
        elif str_tag == 'b':
            self.bd_s=data_schema
            return True
        elif str_tag == 'l':
            self.line_s=data_schema
            return True
        elif str_tag == 'e':
            self.e1_s=data_schema
            self.e2_s=data_schema
            self.e3_s=data_schema
            return True
        else:
            return False

    def __set_canvas__(self,ax):
        e1, = ax.plot([], [], self.e1_s[0], lw=self.e1_s[1])
        e2, = ax.plot([], [], self.e2_s[0], lw=self.e2_s[1])
        e3, = ax.plot([], [], self.e3_s[0], lw=self.e3_s[1])
        w, = ax.plot([], [], [], self.w_s[0], lw=self.w_s[1])
        M, = ax.plot([], [], [], self.m_s[0], lw=self.m_s[1])
        bd, = ax.plot([], [], [], self.bd_s[0], lw=self.bd_s[1])
        line, = ax.plot([], [], [], self.line_s[0], lw=self.line_s[1])

        if self.draw_base_frame:
            ax.plot([0, 1], [0, 0], [0, 0], 'r-', lw=1)
            ax.plot([0, 0], [0, 1], [0, 0], 'r-', lw=1)
            ax.plot([0, 0], [0, 0], [0, 1], 'r-', lw=1)
        return [e1,e2,e3,w,M,line,bd]

    def get_data_from_obj(self,Obj, ell):
        e1 = Obj.N.move_with_origin(Obj.N.e1)
        e2 = Obj.N.move_with_origin(Obj.N.e2)
        e3 = Obj.N.move_with_origin(Obj.N.e3)
        o = Obj.N.origin
        m = Obj.Mo()
        w = Obj.N.move_with_origin(Obj.omega)
        body = Obj.N.get_axes_array().dot(ell)
        return [e1,e2,e3,w,m,o,body]

    def get_data_from_state(self,state,Obj,ell):
        o = state[0]
        e1 = np.add(state[0], state[1].rotate([1, 0, 0]))
        e2 = np.add(state[0], state[1].rotate([0, 1, 0]))
        e3 = np.add(state[0], state[1].rotate([0, 0, 1]))
        rot_mat = np.array(
            [state[1].rotate([1, 0, 0]), state[1].rotate([0, 1, 0]), state[1].rotate([0, 0, 1])]).T
        w = np.add(state[0], rot_mat.dot(state[2]))
        m = np.add(state[0], rot_mat.dot(Obj.Io.dot(state[2])))
        body = rot_mat.dot(ell)
        return [e1, e2, e3, w, m, o, body]

    def __update_canvas__ (self,canvas, Obj, ell, state=None):
        if state is None:
            data=self.get_data_from_obj(Obj,ell)
        else:
            data=self.get_data_from_state(state,Obj,ell)
        e1x, e1y, e1z = data[0]
        e2x, e2y, e2z = data[1]
        e3x, e3y, e3z = data[2]
        w1, w2, w3 = data[3]
        mx, my, mz = data[4]
        ox,oy,oz =data[5]
        body=data[6]

        if self.draw_axes:
            canvas[0].set_data([ox, e1x], [oy, e1y])
            canvas[1].set_data([ox, e2x], [oy, e2y])
            canvas[2].set_data([ox, e3x], [oy, e3y])
            canvas[0].set_3d_properties([oz, e1z])
            canvas[1].set_3d_properties([oz, e2z])
            canvas[2].set_3d_properties([oz, e3z])

        if self.draw_omega:
            canvas[3].set_data([ox, w1], [oy, w2])
            canvas[3].set_3d_properties([oz, w3])

        if self.draw_m:
            canvas[4].set_data([ox, mx], [oy, my])
            canvas[4].set_3d_properties([oz, mz])

        if self.draw_line:
            canvas[5].set_data([0, ox], [0, oy])
            canvas[5].set_3d_properties([0, oz])

        if self.draw_body:
            canvas[6].set_data(body[0] + ox * np.ones(len(body[0])), body[1] + oy * np.ones(len(body[1])))
            canvas[6].set_3d_properties(body[2] + oz * np.ones(len(body[2])))

        return canvas













