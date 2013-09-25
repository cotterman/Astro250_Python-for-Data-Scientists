import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import Rectangle


#obtain x and y coordinates of space that you click on

class FlowerPlot(object):

    """Create a plot that displays traits in grid of scatter plots"""

    # we use a leading _ to indicate that the method is private (
    # ie, should only be called from within the object )
    def _init_plot(self):
        self.f, self.axes = plt.subplots(nrows=4, ncols=4)
        self.f.set_size_inches(18., 12.)
        self.f.suptitle('Flower Characteristics', fontsize='x-large')
                
        # mapping from flower type to color
        ctable = {'setosa':'r','versicolor':'g','virginica':'b'}
        for row, trait1 in enumerate(self.traits):
            for col, trait2 in enumerate(self.traits):
                colors = [ctable[s] for s in self.q3data['species']]
                self.axes[row,col].scatter(
                    self.q3data[trait1], self.q3data[trait2], c=colors )
                
                if col==row:
                    self.axes[row,col].set_title(
                        trait1, position=(.1, .9), 
                        horizontalalignment='left', verticalalignment='top')
        
        return
    
    def _init_rectangles(self):
        self.rectangles = []
        n_row = len(self.axes)
        for row_i, all_axes in enumerate(self.axes):
            self.rectangles.append([])
            for col_i, axes in enumerate(all_axes):
                rect = Rectangle( (0, 0), 0, 0 )
                rect.set_visible(False)
                axes.add_patch(rect)
                self.rectangles[-1].append(rect)
        print self.rectangles
        return

    def _find_axes_coords(self, inaxes):
        for row_i, axes_rows in enumerate(self.axes):
            for col_i, axes in enumerate(axes_rows):
                if axes == inaxes:
                    return (row_i, col_i)
    
    def on_press(self, event):
        self.mouse_on = True 
        self.s_axis_coords = self._find_axes_coords( event.inaxes ) 
        self.s_x = event.xdata
        self.s_y = event.ydata
        
        rect = self.rectangles[self.s_axis_coords[0]][self.s_axis_coords[1]]
        rect.set_width(1)
        rect.set_height(1)
        rect.set_xy((self.s_x, self.s_y))        
        rect.set_visible(True)
        
        event.inaxes.figure.canvas.draw()
        return
    
    def on_release(self, event):
        self.mouse_on = False
        row_i, col_i = self.s_axis_coords
        
        self.rectangles[row_i][col_i].set_visible(False)        
        self.axes[row_i][col_i].figure.canvas.draw()                
        return
    
    def on_motion(self, event):
        event_coords = self._find_axes_coords( event.inaxes )
        #print event.x, event.y, event_coords
        return
    
    # __init__ is called whenever an object instance is initialized
    def __init__(self, data_fname):
        #using self.XXX means that we will store attribute XXX for 
            #in this instance of FlowerPlot
        self.q3data = pd.read_csv(data_fname)
        self.traits = list(self.q3data.columns)[:4]
        self.unique_species = set(self.q3data['species'])
        
        self._init_plot()
        self._init_rectangles()
                
        #register the button_press_event handler
        self.cidpress = self.f.canvas.mpl_connect(
            'button_press_event', self.on_press)
        self.cidrelease = self.f.canvas.mpl_connect(
            'button_release_event', self.on_release)
        self.cidmotion = self.f.canvas.mpl_connect(
            'motion_notify_event', self.on_motion)

        #begin with mouse being in the not pressed state
        #obtain axis and coordinates of mouse when pressed -- call them s_axis and s_x and s_y
        #set f_axis and f_x and f_y equal to the starting positions
        #obtain axis and coordinates of position of mouse while still pressed
            #if f_axis==s_axis:
                #update f_axis, f_x, f_y 
            #else not update coordinates
        #draw rectangle determined as follows:
            #x values between min(s_x, f_x) and max(s_x, f_x) and 
            #y values between min(s_y, f_y) and max(s_y, f_y)
        

        return

# Plot the data in a 4x4 grid
my_plot = FlowerPlot('flowers.csv')
plt.show()

#plt.savefig('q3_flowers_stationary.pdf')

# Interactively draw rectangles on one of the subplots

# Identify the datapoints located within the drawn rectangle

# Change the color/opacities of the corresponding points in the other subplots 


