import vtk
import numpy as np
from lib.simpleFunctions import simpleObjects as sO
import matplotlib.pyplot as plt
from matplotlib import colors as cl

import os, json
from datetime import datetime as dt

# ---------------------------------------------------------
# Global variables are always bad. However, there
# appears to be no good way in which the renderer
# and the window objects can be passed along to 
# other functions while the windoow is being rendered
# ---------------------------------------------------------
renWin = vtk.vtkRenderWindow() # for the screen capture
ren = vtk.vtkRenderer() # for the camera

def restoreCammeraSpecs(fileName):

    try:
        camera = ren.GetActiveCamera()
        data = json.load(open(fileName))
        camera.SetFocalPoint(data['focalPoint'])
        camera.SetPosition(data['position'])
        camera.SetViewUp(data['viewUp'])
        camera.SetViewAngle(data['viewAngle'])
        camera.SetClippingRange(data['clippingRange'])
    except Exception as e:
        print(f'Unable to restore the session from [{fileName}]: {e}')

    return

def saveCameraSpecs():

    camera = ren.GetActiveCamera()
    folder = '../results/cameraPos'
    os.makedirs(folder, exist_ok=True)
    fileName = dt.now().strftime('3D_%Y-%m-%d--%H-%M-%S.json')
    fileName = os.path.join( folder, fileName )

    focalPoint    = [n for n in camera.GetFocalPoint()]
    position      = [n for n in camera.GetPosition()]
    viewUp        = [n for n in camera.GetViewUp()]
    viewAngle     = camera.GetViewAngle()
    clippingRange = [n for n in camera.GetClippingRange()]

    data = {
        'focalPoint'    : focalPoint,      
        'position'      : position,    
        'viewUp'        : viewUp,  
        'viewAngle'     : viewAngle,     
        'clippingRange' : clippingRange,         
    }

    with open(fileName, 'w') as f:
        f.write( json.dumps(data) )

    with open(os.path.join(folder, 'latest3D.json'), 'w') as f:
        f.write( json.dumps(data) )


    print(f'+------------------------------------------')
    print(f'| focalPoint     = {focalPoint}')
    print(f'| position       = {position}')
    print(f'| viewUp         = {viewUp}')
    print(f'| viewAngle      = {viewAngle}')
    print(f'| clippingRange  = {clippingRange}')
    print(f'+------------------------------------------')

    return

def screenShot():

    folder = '../results/screenShots'
    os.makedirs(folder, exist_ok=True)
    fileName = dt.now().strftime('%Y-%m-%d--%H-%M-%S.png')
    fileName = os.path.join( folder, fileName )

    # screenshot code:
    w2if = vtk.vtkWindowToImageFilter()
    w2if.SetInput(renWin)
    w2if.SetInputBufferTypeToRGB()
    w2if.ReadFrontBufferOff()
    w2if.Update()

    writer = vtk.vtkPNGWriter()
    writer.SetFileName(fileName)
    writer.SetInputConnection(w2if.GetOutputPort())
    writer.Write()

    return fileName

def Keypress(obj, event):
    key = obj.GetKeySym()
    if (key == 's') or (key == 'S'):
        fileName = screenShot()
        print(f'Screenshot saved at [{fileName}]')

    if (key == 'c') or (key == 'C'):
        saveCameraSpecs()

def getData():

    data = [
        ["Something","27574","M","Hispanic"],
        ["ArapahoeHouse","11636","M","White"],
        ["Other","32608","M","American Indian"],
        ["ArapahoeHouse","44460","F","White"],
        ["Something","18899","F","White"],
        ["ArapahoeHouse","26025","M","White"],
        ["ArapahoeHouse","7971","M","Hispanic"],
        ["ArapahoeHouse","19373","M","Black"],
        ["ArapahoeHouse","41578","M","White"],
        ["ArapahoeHouse","42446","M","Native American"],
        ["ArapahoeHouse","23182","F","White"],
    ]

    nPatients = len(data)
    nDaysList = [206, 589, 278, 348, 274, 32, 317, 73, 184, 641, 468]

    diagn = [
        [['Anxiety',],['Anxiety',],['Anxiety','MDD',],['MDD',],['MDD',],['MDD',],['MDD',],['MDD',],['Bipolar',],['Bipolar',]],
        [['Alcohol',],['Alcohol',],['Alcohol',],['Bipolar','Alcohol',],['Bipolar','Alcohol',],['Bipolar',],['Bipolar',],['Bipolar',],['Bipolar',],['Bipolar',]],
        [['Alcohol',],['Alcohol',],['Alcohol','MDD',],['Alcohol','MDD',],['Alcohol','MDD',],['Alcohol','MDD',],['Alcohol','MDD',],['MDD',],['MDD',],['Schizo',]],
        [['Alcohol',],['Alcohol',],['Alcohol',],['Alcohol','MDD',],['Alcohol','MDD',],['Alcohol','MDD',],['MDD',],['MDD',],['MDD',],['MDD',]],
        [['MDD',],['MDD',],['MDD',],['Alcohol','MDD',],['Alcohol',],['Alcohol',],['Bipolar','Alcohol',],['Bipolar','Alcohol',],['Bipolar',],['Bipolar',]],
        [['Alcohol',],['Alcohol',],['Alcohol','MDD',],['Alcohol','MDD',],['MDD',],['MDD',],['Bipolar',],['Bipolar',],['Bipolar',],['Bipolar',]],
        [['Schizo',],['Schizo',],['Schizo',],['Schizo',],['Schizo','MDD',],['Schizo','MDD',],['Schizo','MDD',],['Schizo','MDD',],['Schizo','MDD',],['Schizo',]],
        [['Schizo',],['Schizo',],['Schizo',],['Schizo',],['Schizo',],['Schizo',],['Schizo','MDD',],['Schizo','MDD',],['MDD',],['MDD',]],
        [['MDD',],['MDD',],['MDD',],['MDD',],['MDD',],['Alcohol','MDD',],['Alcohol','MDD',],['Alcohol',],['Alcohol',],['Alcohol',]],
        [['Schizo',],['Schizo','MDD',],['MDD',],['MDD',],['MDD',],['MDD',],['MDD',],['Schizo','MDD',],['Schizo',],['Schizo',]],
        [['Schizo',],['Schizo',],['Schizo',],['Schizo','MDD',],['Schizo','MDD',],['MDD',],['MDD',],['MDD',],['MDD',],['Schizo',]],
    ]

    for p in range(nPatients):
        nDays = nDaysList[p]
        data[p].append( np.random.randint(1,7,nDays) )
        data[p].append(diagn[p])

    return data

def colorMapper(forMap):

    uniques = sorted(list(set(forMap)))
    N       = len(uniques)-1
    mapper  = { m:plt.cm.tab20b(i/N) for i, m in enumerate(uniques)}

    result = [ mapper[f][:3] for f in forMap ]

    return result

def colorMapper3D_smooth(forMap):
    
    minVal  = min(map(min, forMap))
    maxVal  = max(map(max, forMap))
    forMap1 = [ (0.2+(np.array(f) - minVal)*0.8/(maxVal - minVal)) for f in forMap]
    forMap2 = [plt.cm.Blues(f)[:,:-1] for f in forMap1]
    
    return forMap2

def sizeMapper3D_smooth(forMap):
    
    minVal  = min(map(min, forMap))
    maxVal  = max(map(max, forMap))
    forMap1 = [ (0.2+(np.array(f) - minVal)*0.8/(maxVal - minVal)) for f in forMap]
    
    return forMap1

def get1Dobjects(colors, xPos, xText = 'x', yPosDelta=0.5, size=0.3, highlight=None):

    allObj = []
    for i, color in enumerate(colors):

        if (highlight is not None) and (highlight != i):
            color = cl.rgb_to_hsv(color)
            # color[0] = 0
            color[1] = 0
            color = cl.hsv_to_rgb(color)

        obj = sO.Cube()
        obj.source.SetCenter(xPos, i*yPosDelta, 0)
        obj.setSize(size)
        obj.setColor( color  )

        if (highlight is not None) and (highlight != i):
            obj.actor.GetProperty().SetOpacity(0.2)

        allObj.append( obj )

    xLabel = sO.Text(f'{xText}')
    xLabel.actor.SetScale( 0.1, 0.1, 0.1 )
    xLabel.actor.SetPosition( xPos-0.2, -1, 0 )
    xLabel.actor.GetProperty().SetColor( 0, 0, 0 )

    allObj.append( xLabel )

    ax1 = sO.Line((xPos,-0.4,0),(xPos,-0.6,0))
    allObj.append( ax1 )

    return allObj

def get1DobjectsSmooth( vals, xPos, xText='x', yPosDelta=0.5, size=0.3, vMax = None, vMin=None, highlight=None ):

    if vMin is None:
        minVal = min(vals)
    else:
        minVal = vMin

    if vMax is None:
        maxVal = max(vals)
    else:
        maxVal = vMax

    size1 = 0.2 + 0.8*(np.array(vals) - minVal)/(maxVal-minVal)
    colors = plt.cm.Blues(size1)[:,:-1]

    allObj = []
    for i, color in enumerate(colors):

        if (highlight is not None) and (highlight != i):
            color = cl.rgb_to_hsv(color)
            # color[0] = 0
            color[1] = 0
            color = cl.hsv_to_rgb(color)

        obj = sO.Cube()
        obj.source.SetCenter(xPos, i*yPosDelta, 0)
        obj.setSize(size*size1[i])
        obj.setColor( color  )

        if (highlight is not None) and (highlight != i):
            obj.actor.GetProperty().SetOpacity(0.2)

        allObj.append( obj )

    xLabel = sO.Text(f'{xText}')
    xLabel.actor.SetScale( 0.1, 0.1, 0.1 )
    xLabel.actor.SetPosition( xPos-0.2, -1, 0 )
    xLabel.actor.GetProperty().SetColor( 0, 0, 0 )

    allObj.append( xLabel )

    ax1 = sO.Line((xPos,-0.4,0),(xPos,-0.6,0))
    allObj.append( ax1 )

    return allObj

def get2DObjects(colors2D, sizes2D, xPos, xText='x', yPosDelta=0.5, zPosDelta=0.5, size=0.3, maxNz=10, highlight=None):

    allObj = []
    for i, (colors, sizes) in enumerate(zip(colors2D, sizes2D)):
        for j, (c, s) in enumerate(zip(colors, sizes)):
            if j > maxNz:
                break

            if (highlight is not None) and (highlight != i):
                c = cl.rgb_to_hsv(c)
                # color[0] = 0
                c[1] = 0
                c = cl.hsv_to_rgb(c)

            obj = sO.Cube()
            obj.source.SetCenter(xPos, i*yPosDelta, -j*zPosDelta)
            obj.setSize(size*s)
            obj.setColor( c )

            if (highlight is not None) and (highlight != i):
                obj.actor.GetProperty().SetOpacity(0.1)

            allObj.append( obj )

    xLabel = sO.Text(f'{xText}')
    xLabel.actor.SetScale( 0.1, 0.1, 0.1 )
    xLabel.actor.SetPosition( xPos-0.2, -1, 0 )
    xLabel.actor.GetProperty().SetColor( 0, 0, 0 )
    allObj.append( xLabel )

    ax1 = sO.Line((xPos,-0.4,0),(xPos,-0.6,0))
    allObj.append( ax1 )


    return allObj

def getPatients(nPatients, xPos, yPosDelta):

    allObj = []
    for p in range(nPatients):
        patientText = sO.Text(f'p_{p:03d}')
        patientText.actor.SetScale( 0.1, 0.1, 0.1 )
        patientText.actor.SetPosition( xPos, p*yPosDelta, 0 )
        patientText.actor.GetProperty().SetColor( 0, 0, 0 )    

        allObj.append( patientText )

        ax = sO.Line((xPos-0.3 -0.1, p*yPosDelta, 0), (xPos-0.3 +0.1, p*yPosDelta, 0))
        allObj.append( ax )

    ax = sO.Line((xPos-0.3, 0, 0), (xPos-0.3, (nPatients-1)*yPosDelta, 0))
    allObj.append( ax )

    return allObj

def getDiagnObjs(diagn, xPos, yPosDelta=0.5, zPosDelta=0.5, size=0.3, highlight=None):

    uniques = set([])
    for ds in diagn:
        for d in ds:
            uniques.update(d)

    uniques = sorted(list(uniques))
    nUniq   = len(uniques)
    colors  = { m:plt.cm.tab20b(i/nUniq)[:-1] for i, m in enumerate(uniques) }
    poss    = { m:i for i, m in enumerate(uniques) }
    
    
    allObj = []
    for i, patient in enumerate(diagn):
        for j, day in enumerate(patient):
            for k, disease in enumerate(uniques):
                if disease in day:

                    c = colors[disease]
                    if (highlight is not None) and (highlight != i):
                        c = cl.rgb_to_hsv(c)
                        c[1] = 0
                        c = cl.hsv_to_rgb(c)
                        


                    obj = sO.Cube()
                    obj.source.SetCenter(xPos -k*size/(nUniq) , i*yPosDelta, -j*zPosDelta)
                    obj.setSize( size/(nUniq + 1)  )
                    obj.setColor( c )

                    if (highlight is not None) and (highlight != i):
                        obj.actor.GetProperty().SetOpacity(0.1)
                    allObj.append( obj )

    return allObj


def plot3D():

    bgColor = [217/255, 211/255, 232/255]

    data = getData()
    site, patient, sex, race, cgi, diagn = zip(*data)
    meanCGI = [np.mean(m[:10]) for m in cgi]
    
    sexColors  = colorMapper( sex )
    raceColors = colorMapper( race )
    siteColors = colorMapper( site )
    cgiColors  = colorMapper3D_smooth( cgi )
    cgiSizes   = sizeMapper3D_smooth( cgi )
    
    ren.SetBackground(bgColor)
    
    renWin.AddRenderer(ren)
    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)


    for obj in getPatients(11, 0, 0.5):
        ren.AddActor( obj.actor )

    for obj in get2DObjects(cgiColors, cgiSizes, -1, 'cgi', highlight=4):
        ren.AddActor( obj.actor )
    
    for obj in getDiagnObjs(diagn, -2, size=1, highlight=4):
        ren.AddActor( obj.actor )


    # for obj in get1DobjectsSmooth( meanCGI, xPos=-2, xText='meanCGI', vMax = 7, vMin=1, highlight=4 ):
    #     ren.AddActor( obj.actor )

    # for obj in get1Dobjects(raceColors, 3, 'race', highlight=4):
    #     ren.AddActor( obj.actor )

    # for obj in get1Dobjects(sexColors, 2, 'sex', highlight=4):
    #     ren.AddActor( obj.actor )
    
    
    # day4 = sO.MeshXY(0,0, 4, 5, -2, 60)
    # ren.AddActor( day4.actor )

    user4 = sO.MeshXZ(-3.3, 0, -0.3, -5, 2, 20)
    ren.AddActor( user4.actor )


    renWin.SetSize(900, 900)
    renWin.SetWindowName('3d stuff')

    iren.AddObserver("KeyPressEvent", Keypress)

    iren.Initialize()

    ren.ResetCamera()
    restoreCammeraSpecs('../results/cameraPos/latest3D.json')
    renWin.Render()

    iren.Start()


    return

