from logs import logDecorator as lD 
import jsonref, pprint
import matplotlib.pyplot as plt
import numpy as np

config = jsonref.load(open('../config/config.json'))
logBase = config['logging']['logBase'] + '.modules.contours.contours'


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

    print(cs.levels)

    # for i, segment in enumerate(cs.allsegs):
    #     print(i, len(segment))
    #     plt.figure()
    #     for j, polygons in enumerate(segment):
    #         print('\t', j, len(polygons))
    #         polygons = np.array(polygons)
    #         x1, y1 = polygons.T 
    #         plt.plot(x1, y1)
    #     plt.xlim([-5, 5])
    #     plt.ylim([-5, 5])
    
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


    doSomething()

    print('Getting out of Module 1')
    print('-'*30)

    return

