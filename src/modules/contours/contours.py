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


def pyVistaLine(result, day):


    grid = pv.UniformGrid()
    n_x, n_y, n_z = result.shape
    grid.dimensions = np.array((n_x-1, n_y-1, n_z-1)) + 1
    grid.origin = (day-3, -6, -6)
    grid.spacing = (6/100, 12/99, 12/99)
    grid.point_arrays['diagnosis'] = result.flatten('F')

    contours1 = grid.contour([0.8], 'diagnosis')
    contours2 = grid.contour([0.5], 'diagnosis')
    contours3 = grid.contour([0.1], 'diagnosis')


    days = np.array([7, 25, 56, 62, 80])
    cgi  = np.array([1, 4, 5,  3, 1])
    l_x = np.random.rand(5)*5
    l_y = np.random.rand(5)*5

    dInt = np.linspace( days.min(), days.max(), 100 )
    cInt = interpolate.interp1d( days, cgi, 'cubic' )( dInt )
    l_xInt = interpolate.interp1d( days, l_x, 'cubic' )( dInt )
    l_yInt = interpolate.interp1d( days, l_y, 'cubic' )( dInt )

    points = np.column_stack((dInt, l_xInt, l_yInt))

    poly = pv.PolyData()
    poly.points = points
    the_cell = np.arange(0, len(points), dtype=np.int)
    the_cell = np.insert(the_cell, 0, len(points))
    poly.lines = the_cell
    
    poly["scalars"] = np.ones( np.shape(cInt) )
    poly["cgi"] = cInt*1e-3

    planes = []
    for d in days:
        p = pv.Plane(center=(d,0,0), direction=(1,0,0), i_size=10, j_size=10)
        p['scalars'] = np.ones(p.n_points)
        planes.append( p )
        

    tube = poly.tube( radius=0.1, scalars='cgi', radius_factor=10 )
    
    sphere = pv.Sphere(center=(25, -3, 3))

    pv.set_plot_theme('document')
    plt = pv.Plotter()
    # plt.background_color = '0xffffff'
    plt.add_mesh( tube, color = 'orange' )
    plt.add_mesh( contours1, color=(0.8, 0, 0), opacity=0.2 )
    plt.add_mesh( contours2, color=(0.5, 0, 0), opacity=0.2 )
    plt.add_mesh( contours3, color=(0.2, 0, 0), opacity=0.2 )
    plt.add_mesh( sphere, color='tan' )

    for plane in planes:
        plt.add_mesh( plane,  color='white', opacity=0.1, show_edges=True, edge_color = 'black' )
    camPos = plt.show()
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

    day = 25
    xVals = day + np.linspace(-3, 3, 101)
    yVals = np.linspace(-6, 6, 100)
    zVals = np.linspace(-6, 6, 100)

    data = [
        [(day,  3,  3), 3],
        [(day,  1,  2), 4],
        [(day,  1, -1), 6],
    ]

    for i, (mu, scale) in enumerate(data):
        temp = createGaussian(xVals, yVals, zVals, mu, scale=scale)
        if i == 0:
            result = temp
        else:
            result += temp

    result = result / result.max()
    pyVistaLine(result, day)

    print('Getting out of Module 1')
    print('-'*30)

    return

