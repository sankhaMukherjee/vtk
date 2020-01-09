import vtk

class MySphere():

    def __init__(self):
        
        self.sphere = vtk.vtkSphereSource()
        self.sphere.SetThetaResolution(100)
        self.sphere.SetPhiResolution(100)

        self.sphereMapper = vtk.vtkPolyDataMapper()
        self.sphereMapper.SetInputConnection( self.sphere.GetOutputPort() )

        self.sphereActor = vtk.vtkActor()
        self.sphereActor.SetMapper( self.sphereMapper )

        return

    def setColor(self, color):
        self.sphereActor.GetProperty().SetColor( color )
        return

    def setResolution(self, resolution=100):
        self.sphere.SetThetaResolution(resolution)
        self.sphere.SetPhiResolution(resolution)
        return

    


def createSphere():


    ren = vtk.vtkRenderer()
    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(ren)
    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)

    allSpheres = []
    for x in range(10):
        for y in range(10):
            for z in range(10):

                sphere = MySphere()
                sphere.sphere.SetCenter(x, y, z)
                sphere.sphere.SetRadius(0.5)
                sphere.setColor([1,0,0])
                sphere.setResolution(10)

                allSpheres.append(sphere)


    for sphere in allSpheres:
        ren.AddActor(sphere.sphereActor)


    renWin.SetSize(300, 300)
    renWin.SetWindowName('Cylinder')

    iren.Initialize()

    ren.ResetCamera()
    # ren.GetActiveCamera().Zoom(1.5)
    renWin.Render()

    # Start the event loop.
    iren.Start()

    return


def cylinderMapper():
    colors = vtk.vtkNamedColors()
    # Set the background color.
    bkg = map(lambda x: x / 255.0, [26, 51, 102, 255])
    colors.SetColor("BkgColor", *bkg)

    # This creates a polygonal cylinder model with eight circumferential
    # facets.
    cylinder = vtk.vtkCylinderSource()
    cylinder.SetResolution(100)

    # The mapper is responsible for pushing the geometry into the graphics
    # library. It may also do color mapping, if scalars or other
    # attributes are defined.
    cylinderMapper = vtk.vtkPolyDataMapper()
    cylinderMapper.SetInputConnection(cylinder.GetOutputPort())

    # The actor is a grouping mechanism: besides the geometry (mapper), it
    # also has a property, transformation matrix, and/or texture map.
    # Here we set its color and rotate it -22.5 degrees.
    cylinderActor = vtk.vtkActor()
    cylinderActor.SetMapper(cylinderMapper)
    cylinderActor.GetProperty().SetColor(colors.GetColor3d("Tomato"))
    cylinderActor.RotateX(30.0)
    cylinderActor.RotateY(-45.0)

    # Create the graphics structure. The renderer renders into the render
    # window. The render window interactor captures mouse events and will
    # perform appropriate camera or actor manipulation depending on the
    # nature of the events.
    ren = vtk.vtkRenderer()
    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(ren)
    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)

    # Add the actors to the renderer, set the background and size
    ren.AddActor(cylinderActor)
    ren.SetBackground(colors.GetColor3d("BkgColor"))
    renWin.SetSize(300, 300)
    renWin.SetWindowName('Cylinder')

    # This allows the interactor to initalize itself. It has to be
    # called before an event loop.
    iren.Initialize()

    # We'll zoom in a little by accessing the camera and invoking a "Zoom"
    # method on it.
    ren.ResetCamera()
    ren.GetActiveCamera().Zoom(1.5)
    renWin.Render()

    # Start the event loop.
    iren.Start()