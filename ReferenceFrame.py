import numpy as np
from RigidBodyRotation.QuatPy import Quaternion
from math import *

class ReferenceFrame:

    def __init__(self, origin,name="undefined"):
        self.name=name
        if len(origin)==3:
            self.origin = np.array(origin, dtype=float)
            self.base_quaternion = Quaternion(1,[0,0,0])
            self.e1 = np.array([1, 0, 0])
            self.e2 = np.array([0, 1, 0])
            self.e3 = np.array([0, 0, 1])
            self.calculate_axes()
        else:
            raise ValueError('Base vector must have length 3')

    def get_axes_array(self):
        return np.array([self.e1,self.e2,self.e3]).T

    def calculate_axes(self):
        self.e1 = np.array(self.base_quaternion.rotate([1, 0, 0]))
        self.e2 = np.array(self.base_quaternion.rotate([0, 1, 0]))
        self.e3 = np.array(self.base_quaternion.rotate([0, 0, 1]))

    def orient_new(self,ax,angle):
        if len(ax)==3:
            ax=np.array(ax)/np.linalg.norm(ax)
            self.base_quaternion=Quaternion(cos(angle/2),sin(angle/2)*ax)
            self.calculate_axes()
            return True
        else:
            return False

    def set_base_quaternion(self,b0,b1,b2,b3):
        self.base_quaternion=Quaternion(b0,[b1,b2,b3])
        self.calculate_axes()

    def set_axes(self,e1,e2,e3):
        if len(e1)==3 and len(e2)==3 and len(e3)==3:
            self.e1=e1
            self.e2=e2
            self.e3=e3
            return True
        else:
            return False

    def move_with_origin(self,vec):
        if len(vec)==3:
            return np.add(vec,self.origin)
        else:
            raise ValueError('Base vector must have length 3')

    def to_this_frame(self,vec):
        if len(vec)==3:
            return np.array([self.e1.dot(vec), self.e2.dot(vec), self.e3.dot(vec)])
        else:
            return False

    def to_base_frame(self,vec):
        if len(vec)==3:
            return self.get_axes_array().dot(vec)
        else:
            return False






