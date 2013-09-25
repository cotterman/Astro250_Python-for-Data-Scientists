import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from mpl_toolkits.basemap import Basemap 

# Data descriptor to make a proper array.
dt1 = [('Date', np.int), ('Value', np.float)]
dt2 = [('Date', np.int), ('Temperature', np.int)]
dyahoo = np.loadtxt('yahoo_data.txt', skiprows=1, dtype=dt1)


# Plot the iris dataset in a 4x4 grid
f, ax = plt.subplots()

# Interactively draw rectangles on one of the subplots

# Identify the datapoints located within the drawn rectangle

# Change the color/opacities of the corresponding points in the other subplots 
