from traits.api import *
import wx

class Counter(HasTraits):
    value =  Int()

#A HasTraits object has an edit_traits() method that creates a graphical panel to edit its attributes. 
#This method creates and returns the panel, but does not start its event loop. 
 #(The panel is not yet "alive", unlike with the configure_traits() method.) 

#command seems strange.....guess we are avoiding using a named instance of Counter??
    #and then wx.PySimpleApp().MainLoop() knows to use the most recently created HasTraits object??
Counter().edit_traits()

#Traits uses the wxWidget toolkit by default to create its widget. 
#They can be turned live and displayed by starting a wx application, and its main loop (ie event loop in wx speech).
#Usually it is not necessary to create the wx application yourself, and to start its main loop, 
 #(traits will do all this for you when the .configure_traits() method is called.)
wx.PySimpleApp().MainLoop()
