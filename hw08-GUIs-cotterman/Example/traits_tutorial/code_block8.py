
import wx

import matplotlib
matplotlib.use('WX')
from matplotlib.backends.backend_wx import FigureCanvasWx as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.backends.backend_wx import NavigationToolbar2Wx

from enthought.traits.api import Any, Instance, Float, Str
from enthought.pyface.api import Widget

class MPLWidget(Widget):
    """ A MatPlotLib PyFace Widget """
    # Public traits
    figure = Instance(Figure)
    axes = Instance('matplotlib.axes.Axes')
    mpl_control = Instance(FigureCanvas)

    # Private traits.
    _panel = Any
    _sizer = Any
    _toolbar = Any

    def __init__(self, parent, **traits):
        """ Creates a new matplotlib widget. """
        # Calls the init function of the parent class.
        super(MPLWidget, self).__init__(**traits)

        self.control = self._create_control(parent)


    def _create_control(self, parent):
        """ Create the toolkit-specific control that represents the widget. """

        # The panel lets us add additional controls.
        if isinstance(parent,wx.Panel):
            self._panel = parent
        else:
            self._panel = wx.Panel(parent, -1, style=wx.CLIP_CHILDREN)
        self._sizer = wx.BoxSizer(wx.VERTICAL)
        self._panel.SetSizer(self._sizer)
        # matplotlib commands to create a figure, and add an axes object
        self.figure = Figure()
        self.axes = self.figure.add_axes([0.05, 0.04, 0.9, 0.92])
        self.mpl_control = FigureCanvas(self._panel, -1, self.figure)
        self._sizer.Add(self.mpl_control, 1, wx.LEFT | wx.TOP | wx.GROW)
        self._toolbar = self._get_toolbar()
        self._sizer.Add(self._toolbar, 0, wx.EXPAND)
        self._sizer.Layout()
        self.figure.canvas.SetMinSize((10,10))
        return self._panel


    def _get_toolbar(self):
        return NavigationToolbar2Wx(self.mpl_control)


if __name__ == "__main__":
    try:
        from enthought.pyface.api import ApplicationWindow, GUI
    except ImportError:
        from enthought.pyface import ApplicationWindow, GUI
    class MainWindow(ApplicationWindow): 
        figure = Instance(MPLWidget)
        def _create_contents(self, parent):
            self.figure = MPLWidget(parent)
            return self.figure.control

    gui = GUI()
    window = MainWindow() 
    from pylab import arange, sin
    x = arange(1,10,0.1)
    window.open()
    axes = window.figure.axes.plot(x,sin(x))
    gui.start_event_loop()

