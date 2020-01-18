from logs import logDecorator as lD
import jsonref
import vtk

config = jsonref.load(open('../config/config.json'))
logBase = config['logging']['logBase'] + '.lib.simpleFunctions.simpleObjects'

class Line():

    def __init__(self, p1, p2):
        
        self.linesPolyData = vtk.vtkPolyData()

        self.pts = vtk.vtkPoints()
        self.pts.InsertNextPoint(*p1)
        self.pts.InsertNextPoint(*p2)

        self.linesPolyData.SetPoints(self.pts)

        self.line0 = vtk.vtkLine()
        self.line0.GetPointIds().SetId(0, 0)
        self.line0.GetPointIds().SetId(1, 1)

        self.lines = vtk.vtkCellArray()
        self.lines.InsertNextCell(self.line0)

        self.linesPolyData.SetLines(self.lines)

        self.namedColors = vtk.vtkNamedColors()
        self.colors = vtk.vtkUnsignedCharArray()
        self.colors.SetNumberOfComponents(3)
        # self.colors.InsertNextTypedTuple(self.namedColors.GetColor3ub("Tomato"))
        self.colors.InsertNextTypedTuple((0,0,0))
        self.linesPolyData.GetCellData().SetScalars(self.colors)
        
        self.mapper = vtk.vtkPolyDataMapper()
        self.mapper.SetInputData( self.linesPolyData )

        self.actor = vtk.vtkActor()
        self.actor.GetProperty().SetLineWidth(2)
        self.actor.SetMapper( self.mapper )
        
        return

class Sphere():

    def __init__(self):
        
        self.source = vtk.vtkSphereSource()
        self.source.SetThetaResolution(100)
        self.source.SetPhiResolution(100)

        self.mapper = vtk.vtkPolyDataMapper()
        self.mapper.SetInputConnection( self.source.GetOutputPort() )

        self.actor = vtk.vtkActor()
        self.actor.SetMapper( self.mapper )

        return

    def setColor(self, color):
        self.actor.GetProperty().SetColor( color )
        return

    def setResolution(self, resolution=100):
        self.source.SetThetaResolution(resolution)
        self.source.SetPhiResolution(resolution)
        return

class Cone():

    def __init__(self):
        
        self.source = vtk.vtkConeCone()
        self.source.SetResolution(100)

        self.mapper = vtk.vtkPolyDataMapper()
        self.mapper.SetInputConnection( self.source.GetOutputPort() )

        self.actor = vtk.vtkActor()
        self.actor.SetMapper( self.mapper )

        return

    def setColor(self, color):
        self.actor.GetProperty().SetColor( color )
        return

    def setResolution(self, resolution=100):
        self.source.SetResolution(resolution)
        return

class Cylinder():

    def __init__(self):
        
        self.source = vtk.vtkCylinderSource()
        self.source.SetResolution(100)

        self.mapper = vtk.vtkPolyDataMapper()
        self.mapper.SetInputConnection( self.source.GetOutputPort() )

        self.actor = vtk.vtkActor()
        self.actor.SetMapper( self.mapper )

        return

    def setColor(self, color):
        self.actor.GetProperty().SetColor( color )
        return

    def setResolution(self, resolution=100):
        self.source.SetResolution(resolution)
        return

    def setSize(self, size):
        self.source.SetHeight(size)
        self.source.SetRadius(size/2)

        return

class Cube():

    def __init__(self):

        self.source = vtk.vtkCubeSource()
        self.source.SetCenter(0,0,0)
        self.source.SetXLength(1)
        self.source.SetYLength(1)
        self.source.SetZLength(1)
        
        self.mapper = vtk.vtkPolyDataMapper()
        self.mapper.SetInputConnection( self.source.GetOutputPort() )

        self.actor = vtk.vtkActor()
        self.actor.SetMapper( self.mapper )

        return

    def setSize(self, size=1):

        self.source.SetXLength(size)
        self.source.SetYLength(size)
        self.source.SetZLength(size)

        return

    def setColor(self, color):
        self.actor.GetProperty().SetColor( color )
        return

class Voxel():

    def __init__(self):

        pts = [
            [0, 0, 0],
            [1, 0, 0],
            [0, 1, 0],
            [1, 1, 0],
            [0, 0, 1],
            [1, 0, 1],
            [0, 1, 1],
            [1, 1, 1],
        ]

        self.points = vtk.vtkPoints()
        self.voxel  = vtk.vtkVoxel()
        self.mapper = vtk.vtkDataSetMapper()
        self.actor  = vtk.vtkActor()

        for i, p in enumerate(pts):
            self.points.InsertNextPoint( *p )
            self.voxel.GetPointIds().SetId(i, i)

        self.ug = vtk.vtkUnstructuredGrid()
        self.ug.SetPoints(self.points)
        self.ug.InsertNextCell(self.voxel.GetCellType(), self.voxel.GetPointIds())

        self.mapper.SetInputData(self.ug)
        self.actor.SetMapper(self.mapper)

        self.actor.GetProperty().SetColor(vtk.vtkNamedColors().GetColor3d("Tomato"))
        self.actor.GetProperty().EdgeVisibilityOn()
        self.actor.GetProperty().SetLineWidth(3)
        self.actor.GetProperty().SetOpacity(.1)

        return

class Text():

    def __init__(self, text='None'):

        self.source = vtk.vtkVectorText()
        self.source.SetText(text)
        self.source.Update()

        self.mapper = vtk.vtkPolyDataMapper()
        self.mapper.SetInputConnection( self.source.GetOutputPort() )

        self.actor = vtk.vtkActor()
        self.actor.SetMapper( self.mapper )

        return 

    def setColor(self, color):
        self.actor.GetProperty().SetColor( color )
        return
