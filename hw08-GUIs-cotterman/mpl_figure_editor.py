
#aka tester5.py

#traits does not provide an editor for every need. 
#If we want to insert a powerful tool for plotting we have to create our own traits editor.
#To do so, we need to translate a wxPython object in a traits editor by providing the corresponding API 
 #(i.e. the standard way of building a traits editor, so that the traits framework can do it automatically.

#Traits editor are created by an editor factory that instanciates an editor class and 
 #passes it the object that the editor represents in its value attribute. 
#It calls the editor int() method to create the wx widget. 

#Here we create a wx figure canvas from a matplotlib figure using the matplotlib wx backend. 
#Instead of displaying this widget, we set its control as the control attribute of the editor. 
#TraitsUI takes care of displaying and positioning the editor.

#The matplotlib figure traits editor created in this example can be imported in a 
 #traitsUI application and combined with the power of traits. 
#This editor allows to insert a matplotlib figure in a traitsUI dialog. 
#It can be modified using reactive programming. 
#However, once the dialog is up and running, you have to call self.figure.canvas.draw() 
 #to update the canvas if you made modifications to the figure. 


import wx

import matplotlib
# We want matplotlib to use a wxPython backend
matplotlib.use('WXAgg')
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.backends.backend_wx import NavigationToolbar2Wx

from traits.api import Any, Instance
from traitsui.wx.editor import Editor
from traitsui.wx.basic_editor_factory import BasicEditorFactory

class _MPLFigureEditor(Editor):

    scrollable  = True

    def init(self, parent):
        self.control = self._create_canvas(parent)
        self.set_tooltip()

    def update_editor(self):
        pass

    def _create_canvas(self, parent):
        """ Create the MPL canvas. """
        # The panel lets us add additional controls.
        panel = wx.Panel(parent, -1, style=wx.CLIP_CHILDREN)
        sizer = wx.BoxSizer(wx.VERTICAL)
        panel.SetSizer(sizer)
        # matplotlib commands to create a canvas
        mpl_control = FigureCanvas(panel, -1, self.value)
        sizer.Add(mpl_control, 1, wx.LEFT | wx.TOP | wx.GROW)
        toolbar = NavigationToolbar2Wx(mpl_control)
        sizer.Add(toolbar, 0, wx.EXPAND)
        self.value.canvas.SetMinSize((10,10))
        return panel

class MPLFigureEditor(BasicEditorFactory):

    klass = _MPLFigureEditor


if __name__ == "__main__":
    # Create a window to demo the editor
    from traits.api import HasTraits
    from traitsui.api import View, Item
    from numpy import sin, cos, linspace, pi

    class Test(HasTraits):

        figure = Instance(Figure, ())

        view = View(Item('figure', editor=MPLFigureEditor(),
                                show_label=False),
                        width=400,
                        height=300,
                        resizable=True)

        def __init__(self):
            super(Test, self).__init__()
            axes = self.figure.add_subplot(111)
            t = linspace(0, 2*pi, 200)
            axes.plot(sin(t)*(1+0.5*cos(11*t)), cos(t)*(1+0.5*cos(11*t)))

    Test().configure_traits()
