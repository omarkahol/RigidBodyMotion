import numpy as np
from math import sqrt

class Quaternion:
    def __init__(self, s, v):
        self.s = s
        if len(v)==3:
            self.v = np.array(v)
        else:
            raise ValueError("length must be 3")

    def sum(self, q):
        return Quaternion(self.s + q.s, np.add(self.v,q.v))

    def prod(self, q):
        return Quaternion(self.s * q.s - self.v.dot(q.v), self.s * q.v + q.s * self.v + np.cross(self.v, q.v))

    def scale(self, l):
        self.s = self.s * l
        self.v = l * self.v
        return self

    def norm(self):
        return sqrt((self.s ** 2) + (self.v[0] ** 2) + (self.v[1] ** 2) + (self.v[2] ** 2))

    def normalize(self):
        return self.scale(self.norm())

    def conjugate(self):
        return Quaternion(self.s, [-self.v[0], -self.v[1], -self.v[2]])

    def inv(self):
        return self.conjugate().normalize()

    def __str__(self):
        return str(self.s) + ' + ' + str(self.v[0]) + 'i + ' + str(self.v[1]) + 'j + ' + str(self.v[2]) + 'k'

    def rotate(self, vec):
        return np.array(self.prod(Quaternion(0, vec)).prod(self.inv()).v)

