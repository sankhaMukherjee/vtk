from logs import logDecorator as lD 
import jsonref, pprint
import matplotlib.pyplot as plt
import numpy as np
from scipy import interpolate 

import pyvista as pv

from matplotlib.tri import Triangulation
from skimage import measure

config = jsonref.load(open('../config/config.json'))
logBase = config['logging']['logBase'] + '.modules.contours.contours'

def createGaussian(xVals, yVals, zVals, mu, sigma=1.0, scale=1):

    mu_x, mu_y, mu_z = mu
    n_x, n_y, n_z = len(xVals), len(yVals), len(zVals)

    x, y, z = np.zeros((n_x, n_y, n_z)), np.zeros((n_x, n_y, n_z)), np.zeros((n_x, n_y, n_z))
    for i, m in enumerate( xVals ):
        x[i, :, :] = m
    for i, m in enumerate( yVals ):
        y[:, i, :] = m
    for i, m in enumerate( zVals ):
        z[:, :, i] = m
    
    result  = (x - mu_x)**2/(2*sigma**2)
    result += (y - mu_y)**2/(2*sigma**2)
    result += (z - mu_z)**2/(2*sigma**2)

    result = scale * (1/np.sqrt(2*np.pi*(sigma**2))) * np.exp( - result )

    return result

def generateDiagnosis1(day, n_x, n_y, n_z, xMin=-3, xMax=3, yMin=-6, yMax=6, zMin=-6, zMax=6, isosurfaces = [0.8, 0.5, 0.1]):

    # -----------------------------------
    # Generate contour data ...
    # -----------------------------------
    xVals = np.linspace( xMin, xMax, n_x) + day
    yVals = np.linspace( yMin, yMax, n_y)
    zVals = np.linspace( zMin, zMax, n_z)

    data = [
        [(day,  3,  3), 3],
        [(day,  1,  2), 4],
        [(day,  1, -1), 6],
    ]

    for i, (mu, scale) in enumerate(data):
        if i == 0:
            result = createGaussian(xVals, yVals, zVals, mu, scale=scale)
        else:
            result += createGaussian(xVals, yVals, zVals, mu, scale=scale)

    result = result / result.max()

    # -----------------------------------
    # Diagnosis contours ...
    # -----------------------------------
    grid = pv.UniformGrid()
    grid.dimensions = np.array((n_x-1, n_y-1, n_z-1)) + 1
    grid.origin     = (day+xMin, yMin, zMin)
    grid.spacing    = (
                    (xMax-xMin)/(n_x-1), 
                    (yMax-yMin)/(n_y-1), 
                    (zMax-zMin)/(n_z-1))
    grid.point_arrays['diagnosis'] = result.flatten('F')


    contours = []
    for iso in isosurfaces:
        contours.append( grid.contour([iso], 'diagnosis') )
    
    return contours

def createUserPathTube(days, cgi, l_x, l_y):

    # +--------------------------------------------------
    # | Interpolate the data so we have a smooth path
    # +--------------------------------------------------
    dInt   = np.linspace( days.min(), days.max(), 100 )
    cInt   = interpolate.interp1d( days, cgi, 'cubic' )( dInt )
    l_xInt = interpolate.interp1d( days, l_x, 'cubic' )( dInt )
    l_yInt = interpolate.interp1d( days, l_y, 'cubic' )( dInt )

    points = np.column_stack((dInt, l_xInt, l_yInt))

    path = pv.PolyData()
    path.points = points
    cells = np.arange(0, len(points), dtype=np.int)
    cells = np.insert(cells, 0, len(points))
    path.lines = cells
    
    path["cgi"] = cInt

    tube = path.tube( radius=0.1, scalars='cgi', radius_factor=10 )

    return tube

def generatePlanes(days):

    planes = []
    for d in days:
        p = pv.Plane(center=(d,0,0), direction=(1,0,0), i_size=10, j_size=10)
        p['scalars'] = np.ones(p.n_points)
        planes.append( p )

    return planes

def pyVistaLine():


    # -----------------------------------
    # User 1 path ...
    # -----------------------------------
    days = np.array([7, 25, 56, 62, 80])
    cgi  = np.array([1, 4, 5,  3, 1])
    l_x  = np.random.rand(5)*5
    l_y  = np.random.rand(5)*5
    
    user1Path = createUserPathTube(days, cgi, l_x, l_y)
    planes = generatePlanes(days)

    diag1Contours = []
    for day in days:
        diag1Contours += generateDiagnosis1(day, n_x=101, n_y=100, n_z=100)
    
    
    axis1 = pv.Arrow(start = (days[-1] + 10, 0, 0), shaft_resolution=100, shaft_radius=0.1, tip_radius=0.4, tip_length=1)
    axis2 = pv.Cylinder(center = (days[-1]/2 + 5, 0, 0), height=days[-1]+10, radius=0.1)


    camPos =  [(7.2988723647972575, 115.81941114646078, -70.39876736181398),
                (41.421526710525654, -5.499646455258194, 5.762645130159154),
                (0.4949719112763291, -0.35785497911618896, -0.7917970832032722)]

    pv.set_plot_theme('document')
    plt = pv.Plotter()

    # Plot the axis
    plt.add_mesh( axis1, color='black' )
    plt.add_mesh( axis2, color='black' )

    plt.add_mesh( user1Path, color = 'orange' )

    plt.add_text('some_text',position=(10, 10), color='purple', font='times')
    plt.add_point_labels([(0,0,0)], ['center'], font_family='times', font_size=10, fill_shape=False)
    
    for diag1 in diag1Contours:
        plt.add_mesh( diag1, color=(0.8, 0, 0), opacity=0.2 )
    
    for plane in planes:
        plt.add_mesh( plane,  color='white', opacity=0.1, show_edges=True, edge_color = 'black' )

    # plt.show_bounds(all_edges=True,)
    
    camPos = plt.show(cpos = camPos)
    print(camPos)

    return

@lD.log(logBase + '.main')
def main(logger, resultsDict):
    '''main function for contours
    
    This function finishes all the tasks for the
    main function. This is a way in which a 
    particular module is going to be executed. 
    
    Parameters
    ----------
    logger : {logging.Logger}
        The logger used for logging error information
    resultsDict: {dict}
        A dintionary containing information about the 
        command line arguments. These can be used for
        overwriting command line arguments as needed.
    '''

    print('='*30)
    print('Main function of contours')
    print('='*30)

    pyVistaLine()

    print('Getting out of Module 1')
    print('-'*30)

    return

