
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
import wx

from scipy import * 
from scipy.ndimage import imread
import scipy.ndimage as ndi

###############################################################################



class Camera(HasTraits):
    """ Camera objects. Implements both the camera parameters controls, and
    the picture acquisition.
    """
    exposure = Float(1, label="Choose desired exposure", desc="exposure")
    gain = Enum(1, 2, 3, label="Select desired gain", desc="gain")
    image_name = Str("hummingbird_0001.jpg", label="Name of file")

    def acquire(self):
        Z = imread(self.image_name)
        Z *= self.exposure
        Z = Z**self.gain
        return(Z)

class AcquisitionThread(Thread):
    """ Acquisition loop. This is the worker thread that retrieves images
    from the camera, displays them, and spawns the processing job.
    """
    wants_abort = False

    def process(self, image):
        """ Spawns the processing job. """
        try:
            if self.processing_job.isAlive():
                self.display("Processing to slow")
                return
        except AttributeError:
            pass
        self.processing_job = Thread(target=process, args=(image,
                                     self.results))
        self.processing_job.start()

    def run(self):
        """ Runs the acquisition loop. """
        img =self.acquire()
        self.display('image captured')
        self.image_show(img)

class ControlPanel(HasTraits):
    """ This object is the core of the traitsUI interface. Its view is
    the right panel of the application, and it hosts the method for
    interaction between the objects and the GUI.
    """
    camera = Instance(Camera, ())
    figure = Instance(Figure)
    start_stop_acquisition = Button("Click to Refresh Image")
    results_string = String()
    acquisition_thread = Instance(AcquisitionThread)
    view = View(Group(
                    Group(
                        Item('start_stop_acquisition', show_label=False ),
                        Item('results_string',show_label=False,
                           style='custom' )),
                Item('camera', style='custom', show_label=False)),
                )

    def _start_stop_acquisition_fired(self):
        """ Callback of the "start stop acquisition" button. This starts
        the acquisition thread, or kills it.
        """
        self.acquisition_thread = AcquisitionThread()
        self.acquisition_thread.display = self.add_line
        self.acquisition_thread.acquire = self.camera.acquire
        self.acquisition_thread.image_show = self.image_show
        self.acquisition_thread.start()

    def add_line(self, string):
        """ Adds a line to the textbox display.
        """
        self.results_string = (string + "\n" + self.results_string)[0:1000]

    def image_show(self, image):
        """ Plots an image on the canvas in a thread safe way.
        """
        self.figure.axes[0].images=[] #why?
        self.figure.axes[0].imshow(image, aspect='auto') #axes[0] refers to a subplot, I think
        wx.CallAfter(self.figure.canvas.draw)

class MainWindowHandler(Handler):
    def close(self, info, is_OK):
        if ( info.object.panel.acquisition_thread
            and info.object.panel.acquisition_thread.isAlive() ):
            info.object.panel.acquisition_thread.wants_abort = True
            while info.object.panel.acquisition_thread.isAlive():
                sleep(1)
            wx.Yield()
        return True

class MainWindow(HasTraits):
    """ The main window, here go the instructions to create and destroy the application. """
    figure = Instance(Figure)
    panel = Instance(ControlPanel)

    def _figure_default(self):
        figure = Figure()
        figure.add_axes([0.05, 0.04, 0.9, 0.92])
        return figure

    def _panel_default(self):
        return ControlPanel(figure=self.figure)

    view = View(HSplit(Item('figure', editor=MPLFigureEditor(),
                            dock='vertical'),
                       Item('panel', style="custom"),
                       show_labels=False,
                      ),
                resizable=True,
                height=0.75, width=0.75,
                handler=MainWindowHandler(),
                buttons=NoButtons)

if __name__ == '__main__':
    MainWindow().configure_traits()


#### My to-do ####

#1) modify tester6.py such that it will read in image files (e.g., hummingbirds)

#2) add image manipulation features

#3) change so that each click on "aquire new image" 
    #will acquire a new image (rather than updating image till you say stop)

#4) get image via image search


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
