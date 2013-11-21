import pymc
import numpy as np
import pandas as pd
import os

### data and data folders ###

HW11_FOLDER = os.path.dirname(os.path.abspath(__file__)) 
DATA_FOLDER = os.path.join(HW11_FOLDER, "hw_11_data")
print "os.path.abspath(__file__): " , os.path.abspath(__file__)
print "HW11_FOLDER: " , HW11_FOLDER
print "DATA_FOLDER: " , DATA_FOLDER

#Read data
aprilD = pd.read_table(DATA_FOLDER + "/laa_2011_april.txt", sep = "\t", header=0, index_col=None)



### get_prior_params ###

#The Beta prior encodes our prior knowledge about baseball batting averages. 
    #The hyperparameters alpha and beta should be chosen to reflect this belief.
    #For this assignment, we will choose alpha and beta based on the 
       #league-wide averages from 2010.
      #In 2010 the mean batting average was 0.255 with variance of 0.0011.
      #Choose alpha and beta to satisfy these prior beliefs

#the mean of the beta distribution is a/(a+b) = .255
#the variance of the beta distribution is ab/[(a+b)**2 * (a+b+1)] = .0011
#we have 2 equations and 2 unknowns.  Solving for a and b, we get:
    #(after some pencil-and-paper algebra)
chunk1 = (.745/.255) / ( (1+(.745/.255))**2 )
chunk2 = .0011 * (1 + (.745/.255) )
a = (chunk1 - .0011) / chunk2
b = a * (.745/.255)
prior_params = (a,b)

#test calculation:
#print "Mean of beta prior (compare to .255): " , a/(a+b)
#print "Var of beta prior (compare to .0011): " , (a*b) /((a+b)**2 * (a+b+1))



### sample_posterior ###

#relevant data
N = aprilD.AB #number of at-bats
num_hits = aprilD.H #number of hits
AVG = aprilD.AVG #batting average
nplayers = aprilD.shape[0] #number of players
print "nplayers: " , nplayers

#prior distribution  --- p(theta)
alpha0 = [prior_params[0]]*nplayers
beta0 = [prior_params[1]]*nplayers

#mu is created as a PyMC stochastic variable
    # it will be treated by the back end as a random number generator
mu = pymc.Beta(name='mu', alpha=alpha0, beta=beta0, value=None, size=nplayers)
#print "Draws from prior (one for each player): " , mu
    
#model --- value of batting average, given theta
@pymc.deterministic(plot=False)
def modelled_p(mu=mu):
    mus = np.zeros(n_count_data)
    mus[:] = mu
    return mus

#likelihood for number of hits
xs = pymc.Binomial('xs', n=N, p=modelled_p, value=num_hits, observed=True)
#print "x values: " , xs


