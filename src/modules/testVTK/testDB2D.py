import vtk, os
import numpy as np, json
from lib.simpleFunctions import simpleObjects as sO
import matplotlib.pyplot as plt

from datetime import datetime as dt

ren = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()


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
    fileName = dt.now().strftime('2D_%Y-%m-%d--%H-%M-%S.json')
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

    with open(os.path.join(folder, 'latest2D.json'), 'w') as f:
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
        ["siteid","id","sex","race"],
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
        ["ArapahoeHouse","37843","M","White"],
        ["ArapahoeHouse","38011","M","White"],
        ["Other","13516","M","White"],
        ["ArapahoeHouse","3074","F","White"],
        ["ArapahoeHouse","2080","M","White"],
        ["ArapahoeHouse","31340","M","Hispanic"],
        ["ArapahoeHouse","36197","M","Hispanic"],
        ["ArapahoeHouse","18847","M","White"],
        ["Something","4028","F","Hispanic"],
        ["ArapahoeHouse","27961","F","Black"],
        ["ArapahoeHouse","27043","M","White"],
        ["ArapahoeHouse","40427","M","White"],
        ["ArapahoeHouse","1824","M","White"],
        ["ArapahoeHouse","24072","M","White"],
        ["ArapahoeHouse","5721","M","CAUCASIAN"],
        ["ArapahoeHouse","18118","M","Native American"],
        ["ArapahoeHouse","28631","M","Hispanic"],
        ["ArapahoeHouse","42785","M","White"],
        ["ArapahoeHouse","13622","M","Hispanic/Mexican"],
        ["ArapahoeHouse","27673","M","Hispanic"],
        ["ArapahoeHouse","17639","F","White"],
        ["ArapahoeHouse","11555","M","Hispanic"],
        ["ArapahoeHouse","9491","M","White"],
        ["ArapahoeHouse","43350","M","White"],
        ["ArapahoeHouse","5770","M","Black"],
        ["ArapahoeHouse","15543","M","White"],
        ["ArapahoeHouse","2715","M","Black"],
        ["ArapahoeHouse","8335","M","White"],
        ["ArapahoeHouse","5133","M","White"],
        ["ArapahoeHouse","39500","M","White"],
        ["ArapahoeHouse","2566","M","Hispanic"],
        ["ArapahoeHouse","45162","F","White"],
        ["ArapahoeHouse","27724","M","Hispanic"],
        ["ArapahoeHouse","42703","M","White"],
        ["ArapahoeHouse","2397","M","White"],
        ["ArapahoeHouse","380","M","White"],
        ["ArapahoeHouse","30539","F","white"],
        ["ArapahoeHouse","8234","M","White"],
        ["ArapahoeHouse","23349","M","Hispanic"],
        ["ArapahoeHouse","1211","M","Asian"],
        ["ArapahoeHouse","44275","M","White"],
        ["ArapahoeHouse","24789","F","White"],
        ["ArapahoeHouse","34709","M","White"],
        ["ArapahoeHouse","31572","F","Black"],
        ["ArapahoeHouse","24722","M","White"],
        ["ArapahoeHouse","13932","M","White"],
        ["ArapahoeHouse","5289","M","White"],
        ["ArapahoeHouse","20178","F","White"],
        ["ArapahoeHouse","38272","M","Black"],
        ["ArapahoeHouse","15127","M","White"],
        ["ArapahoeHouse","14042","M","White"],
        ["ArapahoeHouse","40712","M","Hispanic"],
        ["ArapahoeHouse","44259","M","Hispanic"],
        ["ArapahoeHouse","37027","M","White"],
        ["ArapahoeHouse","12474","M","Black"],
        ["ArapahoeHouse","18627","F","White"],
        ["ArapahoeHouse","9566","M","White"],
        ["ArapahoeHouse","38316","F","Native American"],
        ["ArapahoeHouse","317","M","White"],
        ["ArapahoeHouse","22751","M","White"],
        ["ArapahoeHouse","27691","M","White"],
        ["ArapahoeHouse","38595","M","Hispanic"],
        ["ArapahoeHouse","22978","M","White"],
        ["ArapahoeHouse","23557","M","White"],
        ["ArapahoeHouse","45637","M","Black"],
        ["ArapahoeHouse","3427","M","White"],
        ["ArapahoeHouse","18934","F","White"],
        ["ArapahoeHouse","42763","F","Hispanic"],
        ["ArapahoeHouse","36495","M","White"],
        ["ArapahoeHouse","1991","M","White"],
        ["ArapahoeHouse","37235","M","White"],
        ["ArapahoeHouse","7782","M","Black"],
        ["ArapahoeHouse","36117","M","White"],
        ["ArapahoeHouse","37160","M","White"],
        ["ArapahoeHouse","30110","M","White"],
        ["ArapahoeHouse","14276","M","Biracial"],
        ["ArapahoeHouse","24137","M","Hispanic"],
        ["ArapahoeHouse","39217","M","White"],
        ["ArapahoeHouse","19609","M","White"],
        ["ArapahoeHouse","41687","M","Black"],
        ["ArapahoeHouse","30476","F","White"],
        ["ArapahoeHouse","26882","F","White"],
        ["ArapahoeHouse","38658","M","Hispanic"],
        ["ArapahoeHouse","26285","M","White"],
        ["ArapahoeHouse","20151","M","White"],
        ["ArapahoeHouse","18602","M","White"],
        ["ArapahoeHouse","25960","M","White"],
        ["ArapahoeHouse","4556","M","White"],
        ["ArapahoeHouse","5827","M","white"],
    ]

    return data
    
def colorMapper(forMap):

    uniques = sorted(list(set(forMap)))
    N       = len(uniques)-1
    mapper  = { m:plt.cm.tab20(i/N) for i, m in enumerate(uniques)}

    result = [ mapper[f][:3] for f in forMap ]

    return result

def listToBin(forBin, type='sphere', posDelta=0.2, vPosDelta=0.5, startPos=0, startStr = ''):

    distinct    = sorted(list(set(forBin)))
    distinctPos = { k:( i*posDelta + startPos ) for  i, k in enumerate(distinct)}
    NDist       = len(distinct)

    objects = []

    for i, d in enumerate(distinct):
        myText = sO.Text(f'{startStr}[{d}]')
        myText.actor.SetScale( 0.1, 0.1, 0.1 )
        myText.actor.SetPosition( startPos + i*posDelta, -1, 0 )
        myText.actor.GetProperty().SetColor( 0, 0, 0 )
        myText.actor.RotateZ(-90)

        objects.append(myText)

        vLine = sO.Line((startPos + i*posDelta, -.4, 0), (startPos + i*posDelta, -.6, 0))
        objects.append(vLine)

    vLine = sO.Line((startPos, -.5, 0), (startPos + (NDist-1)*posDelta, -.5, 0))
    objects.append(vLine)

    for i, k in enumerate(forBin):
        s = sO.Sphere()
        s.actor.SetScale( posDelta*0.5 )
        s.actor.SetPosition( distinctPos[k], i*vPosDelta, 0 )
        s.actor.GetProperty().SetColor( 0, 1, 0 )
        objects.append( s )

        for j in range(NDist):
            v = sO.Voxel()
            v.actor.SetPosition( startPos+(j-0.5)*posDelta, (i-0.5)*vPosDelta, -0.5*posDelta )
            v.actor.SetScale( posDelta, vPosDelta, posDelta )
            objects.append( v )
        


    return objects

def plot2D():

    bgColor = [217/255, 211/255, 232/255]
    # bgColor = [219/255, 225/255, 235/255]
    
    Npatients = 10
    
    data = getData()[:Npatients+1]
    header = data[0]
    data = data[1:]
    site, patient, sex, race = zip(*data)
    
    N = len(site)

    
    ren.SetBackground(bgColor)
    renWin.AddRenderer(ren)
    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)


    sexColors = colorMapper( sex )
    raceColors = colorMapper( race )
    siteColors = colorMapper( site )

    for m in listToBin(sex, posDelta=0.4, startPos=4, startStr='sex'):
        ren.AddActor( m.actor )

    for m in listToBin(race, posDelta=0.4, startPos=5, startStr='race'):
        ren.AddActor( m.actor )
    
    # Render the x-axes
    ax1 = sO.Line((1,-0.5,0),(3,-0.5,0))
    ren.AddActor( ax1.actor )
    for i in range(3):
        ax1 = sO.Line((i+1,-0.4,0),(i+1,-0.6,0))
        ren.AddActor( ax1.actor )

    # Render the y-axes
    ax1 = sO.Line((0,0,0),(0,(Npatients-1)*0.5,0))
    ren.AddActor( ax1.actor )
    for i in range(Npatients):
        ax1 = sO.Line((-0.1,i*0.5,0),(0.1,i*0.5,0))
        ren.AddActor( ax1.actor )


    for patient in range(Npatients):

        # Set the names for the patients
        myText = sO.Text(f'p_{patient:04d}')
        myText.actor.SetScale( 0.1, 0.1, 0.1 )
        myText.actor.SetPosition( -1, patient*0.5, 0 )
        myText.actor.GetProperty().SetColor( 0, 0, 0 )
        ren.AddActor( myText.actor )
        
        # set the cohort values
        cohort = sO.Sphere()
        cohort.actor.SetScale( 0.3 )
        cohort.actor.SetPosition(1, patient*0.5, 0)
        cohort.setColor( (0, 1, 0)  )
        ren.AddActor( cohort.actor )

        # set the sex values
        sex = sO.Cube()
        sex.source.SetCenter(2, patient*0.5, 0)
        sex.setSize(0.3)
        sex.setColor( sexColors[patient]  )
        ren.AddActor( sex.actor )

        # set the race values
        race = sO.Cube()
        race.source.SetCenter(3, patient*0.5, 0)
        race.setSize( 0.3 )
        race.setColor( raceColors[patient]  )
        ren.AddActor( race.actor )


    # Set the names for the axes
    for pos, dataType in enumerate(['cohort', 'sex ', 'race']):
        myText = sO.Text(f'{dataType}')
        myText.actor.SetScale( 0.1, 0.1, 0.1 )
        myText.actor.SetPosition( pos+0.8, -1, 0 )
        myText.actor.GetProperty().SetColor( 0, 0, 0 )
        ren.AddActor( myText.actor )

    renWin.SetSize(900, 900)
    renWin.SetWindowName('Cylinder')

    iren.AddObserver("KeyPressEvent", Keypress)
    iren.Initialize()

    ren.ResetCamera()
    restoreCammeraSpecs('../results/cameraPos/latest2D.json')
    renWin.Render()

    # Start the event loop.
    iren.Start()

    
    return 


