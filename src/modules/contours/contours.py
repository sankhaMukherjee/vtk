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

@lD.log(logBase + '.doSomethingElse')
def doSomethingElse(logger):


    x, y = np.meshgrid(np.linspace(-5, 5, 100), np.linspace(-5, 5, 100))
    r = np.sqrt( x**2 + y**2 )
    z = np.sinc( r )

    contours = measure.find_contours( z, 0.1 )
    for c in contours:
        x, y = c.T 
        plt.plot(x, y, '+-')
    # print(contours)
    plt.show()

    return

@lD.log(logBase + '.doSomethingElse1')
def doSomethingElse1(logger):


    x, y, z = np.meshgrid(np.linspace(-5, 5, 20),
                      np.linspace(-5, 5, 20),
                      np.linspace(-5, 5, 5))

    points = np.empty((x.size, 3))
    points[:, 0] = x.ravel('F')
    points[:, 1] = y.ravel('F')
    points[:, 2] = z.ravel('F')

    # Compute a direction for the vector field
    direction = np.sin(points)**3

    # plot using the plotting class
    plobj = pv.Plotter()
    plobj.add_arrows(points, direction, 0.5)
    plobj.show()

    return

@lD.log(logBase + '.doSomething')
def doSomething(logger):
    '''print a line
    
    This function simply prints a single line
    
    Parameters
    ----------
    logger : {logging.Logger}
        The logger used for logging error information
    '''

    x, y = np.meshgrid(np.linspace(-5, 5, 100), np.linspace(-5, 5, 100))
    r = np.sqrt( x**2 + y**2 )
    z = np.sinc( r )

    cs = plt.contourf( x, y, z )
    plt.close()
    print(cs.levels)
    
    for i, segment in enumerate(cs.allsegs):
        print(i, len(segment))
        for j, polygon in enumerate(segment):
            polygon = np.array(polygon)
            # print(polygon.T.shape)
            x1, y1 = polygon.T 
            print(f' -> {j}, {len(polygon):4d}, ({x1[0]:.2f},{y1[0]:.2f}) -> ({x1[-1]:.2f},{y1[-1]:.2f}) ')
    
    
    p1 = cs.allsegs[0][0] # seg 0, poly 0
    p2 = cs.allsegs[1][0] # seg 1, poly 0
    p3 = cs.allsegs[1][1] # seg 1, poly 1

    print('+===========================================')
    for p in p2:
        print(f'| {p[0]:.6f}, {p[1]:.6f}')
    print('+===========================================')

    plt.figure()
    for i, p in enumerate([p1.T, p2.T, p3.T]):
        plt.plot( p[0], p[1], '+-', label=f'{i}' )
        plt.plot( [p[0][0]], [p[1][0]],   'o', mfc='None',mec='k', ms=12)
        plt.plot( [p[0][1]], [p[1][1]],   'o', mfc='None',mec='red', ms=8)
        plt.plot( [p[0][-1]], [p[1][-1]], 's', mfc='None',mec='k', ms=12)
        plt.plot( [p[0][-2]], [p[1][-2]], 's', mfc='None',mec='red', ms=8)
    plt.legend()
    plt.show()

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

