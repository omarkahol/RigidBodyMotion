from ReferenceFrame import ReferenceFrame
from Force import Force
from Object import Object
from DrawingSchema import Drawing_Schema
from math import pi,sqrt
import numpy as np

ref = ReferenceFrame([70,70,70],name='body frame')
ref.orient_new_euler(0,0,0)

obj = Object(1,ref_frame=ref,name="Satellite")

npoints=100
theta = np.linspace(-10,10,npoints)
xs=5*np.cos(theta)
ys=5*np.sin(theta)
zs=0.3*theta

obj.compute_io(xs,ys,zs)
print(obj.Io)


obj.apply_w([1,0,7])
obj.apply_v([10,-10,-10])

mpoint=obj.mass/npoints

r = lambda x,y,z: sqrt((x**2)+(y**2)+(z**2))
GM=50000

farr=[]
for i in range(npoints):
    f=Force([xs[i],ys[i],zs[i]],name='gravity_'+str(i))
    expr = lambda x,y,z,t: -GM*mpoint*np.array([x,y,z])/(r(x,y,z)**3)
    f.add_expression(expr)
    farr.append(f)

obj.apply_forces(farr)
dr=Drawing_Schema(lim=(-80,80))
dr.update_schema('e',('b-',3.5))

obj.integrate_and_draw(np.linspace(0,30,1000),drawing_schema=dr,custom_obj=[xs,ys,zs])