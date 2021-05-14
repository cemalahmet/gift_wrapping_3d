from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import mpl_toolkits.mplot3d as a3
import matplotlib.colors as colors
import pylab as pl
from ConvexHull import Point
from ConvexHull import gift_wrapping
from matplotlib.widgets import Slider
from random import randrange
from timeit import default_timer as timer

# define figure and axes
fig = pl.figure()
ax = a3.Axes3D(fig)

# you could change this
max_number = 100

# Add two sliders
axis_color = 'gold'
initial_numbers = 7
initial_range = 50
# Define
points_slider_ax  = fig.add_axes([0.10, 0.95, 0.25, 0.03], facecolor=axis_color)
points_slider = Slider(points_slider_ax, 'Number of points: ', 4, max_number, valinit = initial_numbers)

# another slider
range_slider_ax = fig.add_axes([0.10, 0.90, 0.25, 0.03], facecolor=axis_color)
range_slider = Slider(range_slider_ax, 'range: ', 5, 100, valinit = initial_range)


number_of_points = 7
range_of_points = 50

# Define an action
def points_sliders_on_changed(val):
    ax.cla()
    gift_wrap( int(val) , range_of_points)
    fig.canvas.draw_idle()
def range_sliders_on_changed(val):
    ax.cla()
    gift_wrap(number_of_points , int(val))
    fig.canvas.draw_idle()
points_slider.on_changed(points_sliders_on_changed)
range_slider.on_changed(range_sliders_on_changed)

# random number
def generate_rand_points(number, difference):
    x = [randrange(difference) for i in range(number)]
    y = [randrange(difference) for i in range(number)]
    z = [randrange(difference) for i in range(number)]

    return [x,y,z]

# drawing algorithm
def gift_wrap(number_of_points,range_of_points):

    #name labels
    ax.set_xlabel('X Axis',fontsize=20, color='green')
    ax.set_ylabel('Y Axis',fontsize=20, color='green')
    ax.set_zlabel('Z Axis',fontsize=20, color='green' )

    # instructions
    ax.text2D(0.45, 0.98, 'Hold LEFT mouse button to ROTATE', transform=ax.transAxes, fontsize=10, color='blue')
    ax.text2D(0.35, 0.96, 'Hold RIGHT mouse button and MOVE UP or DOWN to ZOOM OUT or IN', transform=ax.transAxes, fontsize=10, color='blue')

    #random points
    points = generate_rand_points(number_of_points,range_of_points)

    # 3D scatter plotting function
    scattered_points = ax.scatter(points[0],points[1],points[2], s = 100, c = 'red', alpha = 0.9 )

    # make points proper for convex hull algorithm
    P = []
    i = 0
    while i < number_of_points:
        P.append(Point(points[0][i], points[1][i], points[2][i]))
        i = i + 1

    # call algorithm
    start = timer()


    c_hull = gift_wrapping(P)
    end = timer()
    # print(end - start) # Time in seconds, e.g. 5.38091952400282

     # show number of points and faces
    ax.text2D(0.05, 0.07, '# of points: '+ str(len(points[0])), transform=ax.transAxes, fontsize=10, color='red')
    ax.text2D(0.05, 0.05, '# of faces: '+ str(len(c_hull)), transform=ax.transAxes, fontsize=10, color='red')

    # get faces and its points from hull to 3d renderer
    i = 0
    while i < len(c_hull): # faces in convex hull
        x = []
        y = []
        z = []

        x.append(c_hull[i].points[0].x)
        y.append(c_hull[i].points[0].y)
        z.append(c_hull[i].points[0].z)

        x.append(c_hull[i].points[1].x)
        y.append(c_hull[i].points[1].y)
        z.append(c_hull[i].points[1].z)

        x.append(c_hull[i].points[2].x)
        y.append(c_hull[i].points[2].y)
        z.append(c_hull[i].points[2].z)


        verts = [list(zip(x,y,z))]

        tri = a3.art3d.Poly3DCollection(verts)
        tri.set_color(colors.rgb2hex([0.5,0.5,0.5]))
        tri.set_alpha(0.3)
        ax.add_collection3d(tri)
        i = i + 1
        # if number_of_points < 20:
            # pl.draw()
            # pl.pause(0.1)
    
    pl.show()

gift_wrap(int(points_slider.val),int(range_slider.val))
# gift_wrap(200,10)

