
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
lns1 = ax.plot(dyahoo['Date'], dyahoo['Value'], 
               label='Yahoo! Stock Value', color='b')
lns2 = ax.plot(dgoog['Date'], dgoog['Value'], 
               label='Google Stock Value', color='c')
ax2 = ax.twinx()
lns3 = ax2.plot(dtemps['Date'], dtemps['Temperature'], linestyle='--',
                label='NY Mon. High Temp', color='r')
                               
lns = lns1+lns2+lns3
labs = [l.get_label() for l in lns]
ax.legend(lns, labs, loc='center left', frameon=False, fontsize='small')

ax.set_title('New York Temperature, Google, and Yahoo!', fontsize='x-large', fontname='serif', weight='semibold')
ax.set_xlabel('Date(MJD)')
ax.set_ylabel('Value (Dollars)')
ax2.set_ylabel(r"Temperature ($^\circ$F)")
ax2.set_ylim(-150,100)
ax.set_ylim(0,780)
ax.set_xlim(48800, 55600)

plt.savefig('q2_my_stocks.pdf')


######## minor improvments to make ################

#set proper tick marks (ax.set_xticks)
#shift legend slightly
#match colors for yahoo and google better


