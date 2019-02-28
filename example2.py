from ReferenceFrame import ReferenceFrame
from Force import Force
from Object import Object
from DrawingSchema import Drawing_Schema
from math import pi,sqrt
import numpy as np

ref=ReferenceFrame([0,0,0],name='body_frame')
ref.orient_new([1,1,1],0)

obj=Object(1,ref_frame=ref,Io=np.diag([1,1,2]),name='obj1')
obj.apply_w([0,1,1])

#obj.draw(drawing_schema=Drawing_Schema(dt=1/60,lim=(-2,2),draw_str='mbw'),blit=True,n1=5,n2=5)
obj.integrate_and_draw(np.linspace(0,30,1000),drawing_schema=Drawing_Schema(
    dt=1/60,lim=(-2,2),draw_str='ambw'),blit=True,n1=10,n2=10)