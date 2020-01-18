import vtk
import numpy as np
from lib.simpleFunctions import simpleObjects as sO
import matplotlib.pyplot as plt


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

    uniques = list(set(forMap))
    N       = len(uniques)-1
    mapper  = { m:plt.cm.viridis(i/N) for i, m in enumerate(uniques)}

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
        myText.actor.SetPosition( startPos + i*vPosDelta, -0.5, 0 )
        myText.actor.GetProperty().SetColor( 0, 0, 0 )
        myText.actor.RotateZ(-90)

        objects.append(myText)

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


def plotBasics():

    bgColor = [217/255, 211/255, 232/255]
    # bgColor = [219/255, 225/255, 235/255]
    
    
    data = getData()
    header = data[0]
    data = data[1:]
    site, patient, sex, race = zip(*data)
    
    N = len(site)

    ren = vtk.vtkRenderer()
    ren.SetBackground(bgColor)
    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(ren)
    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)

    Npatients = 10

    sexColors = colorMapper( sex )
    raceColors = colorMapper( race )
    siteColors = colorMapper( site )

    for m in listToBin(sex[:Npatients], posDelta=0.4, startPos=4, startStr='sex'):
        ren.AddActor( m.actor )
    
    for patient in range(Npatients):

        # Set the names for the patients
        myText = sO.Text(f'p_{patient:04d}')
        myText.actor.SetScale( 0.1, 0.1, 0.1 )
        myText.actor.SetPosition( 0, patient*0.5, 0 )
        myText.actor.GetProperty().SetColor( 0, 0, 0 )
        ren.AddActor( myText.actor )

        # set the sex values
        sex = sO.Sphere()
        sex.source.SetCenter(2, patient*0.5, 0)
        sex.source.SetRadius(0.1)
        sex.setColor( sexColors[patient]  )
        sex.setResolution(30)
        ren.AddActor( sex.actor )

        # set the race values
        race = sO.Cube()
        race.source.SetCenter(3, patient*0.5, 0)
        race.setSize( 0.3 )
        race.setColor( raceColors[patient]  )
        ren.AddActor( race.actor )

        # set the site values
        site = sO.Cylinder()
        site.source.SetCenter(1, patient*0.5, 0)
        site.setSize( 0.3 )
        site.setColor( siteColors[patient]  )
        ren.AddActor( site.actor )




    # Set the names for the patients
    for pos, dataType in enumerate(['site', 'sex ', 'race']):
        myText = sO.Text(f'{dataType}')
        myText.actor.SetScale( 0.1, 0.1, 0.1 )
        myText.actor.SetPosition( pos+1, -1, 0 )
        myText.actor.GetProperty().SetColor( 0, 0, 0 )
        ren.AddActor( myText.actor )

    renWin.SetSize(1500, 1500)
    renWin.SetWindowName('Cylinder')

    iren.Initialize()

    ren.ResetCamera()
    # ren.GetActiveCamera().Zoom(1.5)
    renWin.Render()

    # Start the event loop.
    iren.Start()

    
    return 


