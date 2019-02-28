import numpy as np
from ReferenceFrame import ReferenceFrame
class Force:
    def __init__(self, origin, ref_frame=ReferenceFrame([0,0,0],name="force_frame"), name="undefined", expr=lambda x,y,z,t: np.array([0,0,0]), fixed_origin=False):

        if len(origin)==3:
            self.name = name
            self.origin = np.array(origin, dtype=float)
            self.__expr__ = expr
            self.fixed_origin=fixed_origin
            self.N=ref_frame
        else:
            raise ValueError('length must be three')

    def add_expression(self,expr):
        try:
            expr(-1,-1,-1,0)
            self.__expr__=expr
        except:
            raise ValueError("The force must be like lambda x,y,z,t: np.array([Fx,Fy,Fz]). If it constant just write lambda x,y,z,t: np.array([a,b,c])")

    def set_origin(self,origin):
        if len(origin)==3:
            self.origin=origin
            return True
        else:
            return False

    def set_reference_frame(self,ref_frame):
        self.N=ref_frame

    def __compute_torque__(self,t0, from_origin, sel_origin):
        return np.cross(sel_origin,self.__apply_force__(t0,from_origin,sel_origin))

    def __str__(self):
        return "Force tag: "+self.name

    def __apply_force__(self,t0,from_origin,sel_origin):
        if t0 >= 0:
            return np.array(self.__expr__(*np.add(sel_origin,from_origin),t0))
        else:
            raise ValueError('Negative time not accepted')

    def apply(self,t):
        return self.__apply_force__(t,self.N.origin,self.origin)

    def torque(self, t):
        return self.__compute_torque__(t,self.N.origin,self.origin)




