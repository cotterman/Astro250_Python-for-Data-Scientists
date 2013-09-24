
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from mpl_toolkits.basemap import Basemap 

#Read in data (data produced in Stata)
q1data = pd.read_csv('HS_data_to_map.csv') #produce dataframe
q1data.index.name = 'Schools' #name the index (i.e., what the rows of the data represent)
print q1data.head()

#training_start_yr float  %9.0g                  first school year affected by onsite HSP
#training_last_yr  float  %9.0g                  school year of last onsite HSP
#cds_code          str14  %14s                   unique school identifier
#school_status     str11  %11s                   Onsite status, or else online only
#latitude          float  %9.0g                  Latitude
#longitude         float  %9.0g                  Longitude
#district          str61  %61s                   District
#enr2011           float  %9.0g                  enrollment within cds_code (school-level),according to race data 
#FRPMpct2011       float  %9.0g                  percent of students enrolled in free and reduced price lunch

#Get subset of data to map
    #participants have school_status=="Active" (285) | school_status=="Graduated" (91) | school_status=="Dropped" (28)
    #note: most "Dropped" schools have a start year, as they are schools that started and then dropped out of program
#q1data[['latitude','longitude']][q1data.school_status=="Dropped"] #get subset of data
#q1data.ix[q1data.school_status=="Dropped", ['latitude','longitude']] #equivalent to line above
sdata = q1data.ix[q1data.school_status=="Dropped", ['latitude','longitude','training_start_yr']] 

#Map locations of participating schools using latitude and longitude
    #Create your Basemap with 'i' resolution, otherwise it will take forever to draw.
# Draw the stations on a real map of the Earth.
# Find boundaries 
lon0 = 0.995*sdata['longitude'].min()
lon1 = 1.01*sdata['longitude'].max()
lat0 = 0.995*sdata['latitude'].min()
lat1 = 1.01*sdata['latitude'].max()

# Geographic grid to draw
parallels = np.linspace(lat0, lat1, 5)
meridians = np.linspace(lon0, lon1, 5)

# Resolution of the basemap to load ('f' is *very* expensive)
resolution = 'i' # intermediate resolution for map info

# Create the figure
f2, ax2 = plt.subplots(figsize=(10,6))

# Make the map object, where we draw geographic information
m = Basemap(lon0, lat0, lon1, lat1, resolution=resolution, ax=ax2)
#m.drawmapboundary(fill_color='#99ffff')
#m.fillcontinents(color='#cc9966',lake_color='#99ffff')
m.drawcoastlines()
m.drawstates()
m.drawcountries()


# Now draw a scatter plot on the same map
m.scatter(sdata['longitude'], sdata['latitude'], marker='o', color='k')
# Add a colorbar to the figure, linked to the scatterplot color scale
#f2.colorbar(s)

# Label the figure and every point by its station label
plt.title('Onsite Healthy Schools Program Participation',fontsize=12)
#for record in tab:
 #   ax2.text( record['lon']+0.04, record['lat']+0.04, record['station'], 
  #          weight='bold', color='yellow', zorder=10)

#Indicate training_start_yr using colors

#save plot
plt.savefig('q1_python_produced.pdf')

###### Other maps that would be cool to make: ########

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

