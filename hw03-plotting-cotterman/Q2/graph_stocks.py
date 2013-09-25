
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from mpl_toolkits.basemap import Basemap 

# Data descriptor to make a proper array.
dt1 = [('Date', np.int), ('Value', np.float)]
dt2 = [('Date', np.int), ('Temperature', np.int)]
dyahoo = np.loadtxt('yahoo_data.txt', skiprows=1, dtype=dt1)
dyahoo.dtype
dyahoo[:10]
dgoog = np.loadtxt('google_data.txt', skiprows=1, dtype=dt1) 
dgoog[:10]
dtemps = np.loadtxt('ny_temps.txt', skiprows=1, dtype=dt2) 
dtemps[:10]

f, ax = plt.subplots()
ax.plot(dyahoo['Date'], dyahoo['Value'], label='Yahoo! Stock Value')
ax.plot(dgoog['Date'], dgoog['Value'], label='Google Stock Value')
#ax.plot(dtemps['Date'], dtemps['Temperature', label='NY Mon. High Temp')
ax.set_title('New York Temperature, Google, and Yahoo!')
ax.set_xlabel('Date(MJD)')
ax.set_ylabel('Value (Dollars)')
ax.legend(loc='center left')

plt.savefig('q2_my_stocks.pdf')

