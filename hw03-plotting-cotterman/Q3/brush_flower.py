import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# Read in data

q3data = pd.read_csv('flowers.csv')


# Plot the iris dataset in a 4x4 grid

traits = list(q3data.columns)[:4]
unique_species = set(q3data['species'])
#print unique_species
#print len(traits)
ctable = {'setosa':'r','versicolor':'g','virginica':'b'}
ctable['versicolor']

f, axes = plt.subplots(nrows=4, ncols=4)

for row, trait1 in enumerate(traits):
    for col, trait2 in enumerate(traits):
        axes[row,col].scatter(q3data[trait1], q3data[trait2], c=[ctable[s] for s in q3data['species']])

axes[0,0].set_title('Flower Characteristics')

#save plot
plt.savefig('q3_flowers_stationary.pdf')



# Interactively draw rectangles on one of the subplots

# Identify the datapoints located within the drawn rectangle

# Change the color/opacities of the corresponding points in the other subplots 
