###############################################################################
## 
## Goal: Estimate a hitter's true batting average, mu_i, (for the entire
## season) from the first month of data.  Use a beta prior for mu_i and
## and MCMC sampler to get a binomial posterior.
##
## Author: Carolyn Cotterman
##
###############################################################################

import pymc
import numpy as np
import pandas as pd
import os

###############################################################################

# leads to subfolder of path of script
    # os.path.abspath takes a pathname, which can be partial or even blank, 
        # and returns a fully qualified pathname.
        # in this case, we get back the path, including /predict_batting_mcmc.py 
    # os.path.dirname takes a filename as a string and returns the directory path portion.
        # so it drops the /predict_batting_mcmc.py portion returned by as.path.abspath
HW11_FOLDER = os.path.dirname(os.path.abspath(__file__)) 
DATA_FOLDER = os.path.join(HW11_FOLDER, "hw_11_data")
print "os.path.abspath(__file__): " , os.path.abspath(__file__)
print "HW11_FOLDER: " , HW11_FOLDER
print "DATA_FOLDER: " , DATA_FOLDER


def get_MLEs(aprilD):
    """ Calculate the MLEs for batting average (mu_i) using data from April
    """
    #the MLE for batting average is equal to the number of hits divided by
        # the number of times at bat.  This number is already in the data.
    print "\nMLEs for batting average using April Data:\n" , aprilD[["Player", "AVG"]]
    


###############################################################################

def main():

    #Read data
    aprilD = pd.read_table(DATA_FOLDER + "/laa_2011_april.txt", sep = "\t", header=0, index_col=None)
    fullD = pd.read_table(DATA_FOLDER + "/laa_2011_full.txt", sep = "\t", header=0, index_col=None)

    #1) Find the MLE of mu_i for each player from the April data.
    get_MLEs(aprilD)

    #2) Draw a sample from the posterior (of size > 1000) assuming a Beta 
        # prior for each mu_i 

        # The Beta prior encodes our prior knowledge about baseball batting averages. 
        # The hyperparameters alpha and beta should be chosen to reflect this belief.
        # For this assignment, we will choose alpha and beta based on the 
          # league-wide averages from 2010.
          # In 2010 the mean batting average was 0.255 and the variance 
            # between players was 0.0011.
          # Choose alpha and beta to satisfy these prior beliefs!

    #3) Check convergence of your MCMC sampler by looking at the trace plots 
        # for at least 3 of the mu_i

    #4) Compute the posterior mean and posterior 95% CI for each mu_i
        # For how many of the 13 players does the full-season batting average 
        # fall within the 95% CI?

    #5) Make the following plots:
        #1. The full-season batting average of each player versus the MLE from (a)
        #2. The full-season batting average of each player versus the posterior mean from (d) 
            #(Include error bars to show the 95% CI).


main()
