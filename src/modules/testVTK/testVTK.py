from logs import logDecorator as lD 
import jsonref, pprint

from modules.testVTK import examples, testDB2D, testDB3D, testDB3D_1

config = jsonref.load(open('../config/config.json'))
logBase = config['logging']['logBase'] + '.modules.testVTK.testVTK'


@lD.log(logBase + '.doSomething')
def doSomething(logger):
    '''print a line
    
    This function simply prints a single line
    
    Parameters
    ----------
    logger : {logging.Logger}
        The logger used for logging error information
    '''

    try:


        # examples.cylinderMapper()
        # examples.createSphere()
        config = {
            'ohe' : True
        }
        # testDB2D.plot2D(config)

        config = {
            'highlight' : 4,
            'race'      : True,
            'sex'       : True,
            'cgi'       : True,
            'meanCGI'   : True
        }
        testDB3D.plot3D(config)

        config = {
            'highlight'  : 4,
            'cgi'        : True,
            'diagn'      : True,
            'cond'       : True,
            'CGI-others' : True,
            'mesh'       : True,
            'mesh-red'   : True,
        }
        # testDB3D_1.plot3D(config)
        
        
    except Exception as e:
        print(f'Problem with the test functionality: {e}')

    return

@lD.log(logBase + '.main')
def main(logger, resultsDict):
    '''main function for testVTK
    
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
    print('Main function of testVTK')
    print('='*30)
    print('We get a copy of the result dictionary over here ...')
    pprint.pprint(resultsDict)

    doSomething()

    print('Getting out of testVTK')
    print('-'*30)

    return

