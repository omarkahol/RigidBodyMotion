# RigidBodyMotion
A handful of classes for representing the motion of a rigid body in a given force field. Rotations are computed with Quaternions.

REFERENCE FRAME
This class is used to represent a reference frame that will be attached to an object. The constructor accepts a name and
an origin. We can further orient our frame calling the method set_base_quaternion (that accepts a transformation quaternion)
or by calling orient_new which accepts the axes of rotation and the angle by which the frame will be rotated.
That class contains the set_axes method which is called automatically after a new base quaternion is introduced and computes
the frame axes. The class contains some other methods to quickly express a vector in the current frame or the base frame.

FORCE
The force class is used to define a force. Generally speaking, we can represent a force by using a function that returns a
vector of length 3. A class is useful as there are many other thing to keep track of, for example the origin (which is essential
to compute its torque) or the possibility to move the origin with the rigid body subjected to that force.
The user must provide an origin and an expression (which can be added in the constructor or with a method) which is a
lambda x,y,z,t -> [f1,f2,f3] even if the force does not depend on one or more inputs

OBJECT
An object must have a mass, its reference frame and an inertia matrix. This last one can be set manually by passing a 
3x3 matrix or calculeted with the method compute_io (compute inertia operator) which accepts the x,y and z coordinates of all
the points of the object. The object can then have an initial and angular velocity (both expressed with a vector of length 3). 
The method apply_forces allows us to set an array of forces applied to the body. The object can then be drawn and animated in 
two ways
 1) draw -> real time animation, the state of the system is integrated and then plotted in real time
 2) integrate_and_draw -> first the state is integrated (the total time must be a parameter) and then drawn

to use both ways we must provide an object called drawing schema which is basically a class that stores 
what and how must be plotted.
