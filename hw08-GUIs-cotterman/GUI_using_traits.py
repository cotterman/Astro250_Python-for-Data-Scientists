
###############################################################################
# Overview: creates GUI which allows user to search for an image online
# and manipulate the image. 
# Author: Carolyn Cotterman
###############################################################################

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.widgets as wg
from matplotlib.widgets import RectangleSelector


###############################################################################

def main():

    #Using Traits and TraitsUI create a GUI application that consists of a
    #search box, a text display, an image display, and a series of buttons.
    
    try:
	    from enthought.traits.api import HasTraits, Str, \
                Int, Directory, RGBColor, Float, Array, Enum
	    from enthought.traits.ui.api import View, Item, Group
    except:
	    from traits.api import HasTraits, Str, \
                Int, Directory, RGBColor, Float, Array, Enum
	    from traitsui.api import View, Item, Group

    class MyImage(HasTraits):
        name = Str
        location = Array()
        color = Enum("Unchanged","Gray-scale",default="Unchanged")
        rotation = Enum("None","Clockwise90",default="None")
        datadir = Directory("./")
        
    bird = MyImage(name="Bird")

    #bring up dialog to edit objects’ attributes specified in class definition
    bird.configure_traits()	

    #The application will accept search strings in the search box and then
    #run an internet image search. The first returned image from the
    #search will be downloaded, the image url displayed in the text
    #display field, and the actual image displayed in the image display
    #field.

    #The buttons will provide the user interface to run the image search as
    #well as perform manipulations on the image currently stored in the
    #display (for example, blurring or rotation). Provide at least three
    #unique (and interesting) image manipulation functions.

    #Tips: Feel free to use an image search (or, include support for
    #multiple different searches). Yahoo has a convenient search module.
    #There is also freedom in how you display the image, but matplotlib
    #is recommended.

main()


