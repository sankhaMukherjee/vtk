from logs import logDecorator as lD 
import jsonref, pprint
import matplotlib.pyplot as plt
import numpy as np

import pyvista

from matplotlib.tri import Triangulation
from skimage import measure

config = jsonref.load(open('../config/config.json'))
logBase = config['logging']['logBase'] + '.modules.contours.contours'

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
    plobj = pyvista.Plotter()
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


    doSomethingElse1()

    print('Getting out of Module 1')
    print('-'*30)

    return

