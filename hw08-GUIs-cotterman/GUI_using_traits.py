
###############################################################################
# Overview: creates GUI which allows user to search for an image online
# and manipulate the image. 
# Author: Carolyn Cotterman
###############################################################################

from threading import Thread
from time import sleep
from traits.api import *
from traitsui.api import View, Item, Group, HSplit, Handler
from traitsui.menu import NoButtons
from mpl_figure_editor import MPLFigureEditor
from matplotlib.figure import Figure
from scipy import * 
import wx

###############################################################################

#### My to-do ####

#1) modify tester6.py such that it will read in image files (e.g., hummingbirds)

#2) add image manipulation features

#3) if there is time, change so that each click on "aquire new image" 
    #will acquire a new image (rather than updating image till you say stop)

#4) if there is still time, figure out how to get image via image search


##################### Original directions #####################################

    #Using Traits and TraitsUI create a GUI application that consists of a
    #search box, a text display, an image display, and a series of buttons.

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

