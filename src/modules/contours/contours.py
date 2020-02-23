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

    x, y, z = np.meshgrid(xVals, yVals, zVals)

    result  = (x - mu_x)**2/(2*sigma**2)
    result += (y - mu_y)**2/(2*sigma**2)
    result += (z - mu_z)**2/(2*sigma**2)

    result = scale * (1/np.sqrt(2*np.pi*(sigma**2))) * np.exp( - result )

    return result


def pyVistaLine():

    days = np.array([7, 25, 56, 62, 80])
    cgi  = np.array([1, 4, 5,  3, 1])
    l_x = np.random.rand(5)
    l_y = np.random.rand(5)

    dInt = np.linspace( days.min(), days.max(), 20 )
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
    
    pv.set_plot_theme('document')
    plt = pv.Plotter()
    # plt.background_color = '0xffffff'
    plt.add_mesh( tube, color = 'orange' )

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

    day = 7
    xVals = day + np.linspace(-3, 3, 101)
    yVals = np.linspace(-6, 6, 100)
    zVals = np.linspace(-6, 6, 100)

    data = [
        # [(day,  3,  3), 7],
        # [(day, -3,  3), 6],
        # [(day, -3,  3), 4],
        [(day,  0,  0), 4],
        [(day, -6, -6), 4],
        [(day,  6,  6), 4],
    ]

    results = []
    for i, (mu, scale) in enumerate(data):
        temp = createGaussian(xVals, yVals, zVals, mu, scale=scale)
        results.append(temp)
        if i == 0:
            result = temp
        else:
            result += temp


    for r in results:
        plt.figure()
        plt.contourf( r[ 50 ,:,:] )
        plt.figure()
        plt.contourf( r[ :,50,:] )
    plt.show()
    # pyVistaLine()

    print('Getting out of Module 1')
    print('-'*30)

    return

