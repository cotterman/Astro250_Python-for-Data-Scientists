
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from mpl_toolkits.basemap import Basemap 



#Read in data (data produced in Stata)
q1data = pd.read_csv('HS_data_to_map.csv') #produce dataframe
q1data.index.name = 'Schools' #name the index (i.e., what the rows of the data represent)
q1data.head()

# Use known boundaries of California 
lon0 = -125
lon1 = -114
lat0 = 32
lat1 = 42

# Create your Basemap with 'i' resolution, otherwise it will take forever to draw. 
    #('f' is *very* expensive)
resolution = 'i' # intermediate resolution for map info

# Create the figure
f2, ax2 = plt.subplots(figsize=(10,6))

# Make the map object, where we draw geographic information
m = Basemap(lon0, lat0, lon1, lat1, resolution=resolution, ax=ax2)
m.drawcoastlines()
m.drawstates()
m.drawcountries()


# Draw a scatter plot on the same map
    #Indicate training_start_yr using colors
s2006 = ax2.scatter(q1data.ix[q1data.training_start_yr==2006,'longitude'], 
                   q1data.ix[q1data.training_start_yr==2006,'latitude'], color='r')
s2007 = ax2.scatter(q1data.ix[q1data.training_start_yr==2007,'longitude'], 
                   q1data.ix[q1data.training_start_yr==2007,'latitude'], color='y')
s2008 = ax2.scatter(q1data.ix[q1data.training_start_yr==2008,'longitude'], 
                   q1data.ix[q1data.training_start_yr==2008,'latitude'], color='g')
s2009 = ax2.scatter(q1data.ix[q1data.training_start_yr==2009,'longitude'], 
                   q1data.ix[q1data.training_start_yr==2009,'latitude'], color='c')
s2010 = ax2.scatter(q1data.ix[q1data.training_start_yr==2010,'longitude'], 
                   q1data.ix[q1data.training_start_yr==2010,'latitude'], color='b')
s2011 = ax2.scatter(q1data.ix[q1data.training_start_yr==2011,'longitude'], 
                   q1data.ix[q1data.training_start_yr==2011,'latitude'], color='m')

ax2.legend((s2006, s2007, s2008, s2009, s2010, s2011), 
          ('2006-2007', '2007-2008', '2008-2009', '2009-2010', '2010-2011', '2011-2012'),
          loc = 'upper right',title="First year of participation", scatterpoints=1)

plt.title('Onsite Healthy Schools Program Participation',fontsize=16)

#save plot
plt.savefig('q1_python_produced.pdf')



#################################################################
###### Related maps that would be cool to make in future ########
#################################################################

    #same as above, but:
        #add in school_status=="Online only" schools (in gray -- they do not have known start year)
        #add in school_status=="none" schools (in black)
    #same as above, but with size of dots indicating enrollment of 5th+7th+9th graders 
        #would need to get from race files (or from fitness grame when it comes in) 
 
    #map FRPMpct2011 of all schools with darker colors indicating higher levels of FRPM
        #range from light red to dark red for HS online participants
        #range from light green to dark green for HS online participants
        #range from light blue to dark blue for non-participants

    #map HS "dosage"?

