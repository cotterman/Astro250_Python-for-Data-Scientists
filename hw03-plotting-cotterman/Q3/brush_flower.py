import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

class FlowerPlot(object):

    """Create a plot that displays traits in grid of scatter plots"""

    # we use a leading _ to indicate that the method is private (
    # ie, should only be called from within the object )
    def _init_plot(self):
        self.f, self.axes = plt.subplots(nrows=4, ncols=4)
        self.f.set_size_inches(18., 12.)
        self.f.suptitle('Flower Characteristics', fontsize='x-large')

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

    # __init__ is called whenever an object instance is initialized
    def __init__(self, data_fname):
        self.q3data = pd.read_csv(data_fname)
        self.traits = list(self.q3data.columns)[:4]
        self.unique_species = set(self.q3data['species'])

        # mapping from flower type to color
        self._init_plot()
        return

# Plot the data in a 4x4 grid
my_plot = FlowerPlot('flowers.csv')

# plt.savefig('q3_flowers_stationary.pdf')

# Interactively draw rectangles on one of the subplots

# Identify the datapoints located within the drawn rectangle

# Change the color/opacities of the corresponding points in the other subplots 


