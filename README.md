-----------------------HOW TO INSTALL----------------------

An IDE that supports Python programming language is needed.
We suggest Microsoft Visual Studio as an IDE.

Program can be opened via IDE by starting "Main.py" file.

-----------------------USER INTERFACE----------------------

After opening the program, it is recommended to make it fullscreen.

With "number of points" slider, the total number of points can be changed.
With "range" slider, the range of points can be changed (from 0 to value)
"# of points" and "# of faces" texts show total number of points and faces.

To ROTATE, hold left mouse button.
To ZOOM IN/OUT, hold right mouse button and drag up or down.

-----------------------REQUIRED LIBRARIES------------------

mpl_toolkits
matplotlib
pylab
random
timeit
queue
math
numpy

--------------------------DATABASES------------------------

We create random numbers in our program 
so any external database is not needed

=============WHAT WE SUCCESSFULLY IMPLEMENTED================

Our program supports:
+ Simple, functional and detailed user interface
+ Display necessary information
+ Zoom in and out
+ Adjust range of points
+ Generate and show randomly generated points in 3D
+ Generate and show faces and borders of convex hull

=================WHAT WE COULD NOT COMPLETE==================

Rendering Engine:
- Due to technical limitations of matplotlib library,
  rendering over 100 face and points is very slow and sometimes it crashes
- We adjusted border and face colors to be seen clearly but in some monitors it maybe unclear

Convex Hull Algorithm:
- Our convex hull implementation sometimes stops and give us few faces.
- Our convex hull implementation sometimes generate more faces inside the convex hull