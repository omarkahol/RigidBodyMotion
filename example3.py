from ReferenceFrame import ReferenceFrame
from Force import Force
from Object import Object
from DrawingSchema import Drawing_Schema
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
from math import pi,sqrt
import numpy as np

mu=3.98e-4
m=100000
r=lambda x,y,z: sqrt((x**2)+(y**2)+(z**2))
rt=6.373
orb=[0,rt+0.405,0]
v=[-0.00766,0.0001,0]

N=ReferenceFrame(orb,name='iss')
iss=Object(m,ref_frame=N,Io=np.diag([50,50,50]),name='iss')
f=Force([0,0,0],ref_frame=N,name='gravity')

f.add_expression(lambda x,y,z,t: -mu*m*np.array([x,y,z])/(r(x,y,z)**3))
iss.apply_forces([f])
iss.apply_w([0.005,0.007,0.006])
iss.apply_v(v)

#DISEGNAMO LA TERRA
t,f=np.meshgrid(np.linspace(0,pi,200),np.linspace(0,2*pi,200))
xs=rt*np.sin(t)*np.cos(f)
ys=rt*np.sin(t)*np.sin(f)
zs=rt*np.cos(t)

fig=plt.figure()
ax=fig.add_subplot(111,projection='3d',aspect='equal',xlim=(-10,10),ylim=(-10,10),zlim=(-10,10))
ax.plot_wireframe(xs,ys,zs,'g-',lw=0.1)

#INTEGRIAMO LA SOLUZIONE
iss.integrate_and_draw(np.linspace(0,86_400,10000),drawing_schema=Drawing_Schema(draw_str='wb'),interval=1,draw_before=[fig,ax],blit=True)


