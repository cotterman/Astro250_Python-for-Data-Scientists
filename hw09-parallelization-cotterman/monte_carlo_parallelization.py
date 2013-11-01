
###############################################################################
#
# Overview: For this homework I run the same algorithm under different
# parallelization methods and evaluate the speedups (execution
# time). I compare simple serial (no parallelization),
# multiprocessing, and IPython’s parallel module.
#
# Author: Carolyn Cotterman
#
###############################################################################

from random import uniform
from math import sqrt
from time import time


def main():

    #Use a Monte Carlo dart-throwing simulation to calculate a 
    #numerical approximation to Pi withou parallelization. 

    #Run algorithm under different parallelization methods. 
    #Run several trials with different numbers of darts
    #thrown (up to execution times ~100 seconds). Keep track of the
    #execution times as a function of number of darts and method of
    #parallelization. Also, keep track of the simulation rate (darts thrown per
    #second). 

    number_of_darts = 1000

    #1) No parallelization

    #2) Python multiprocessing (use the pool function). 

    #3) IPython parallel 
    

    #Plot execution time and simulation rate as a function of number of darts
    #for all three methods. If you calculated standard deviations, use errorbar
    #plots. See the example plot on the following page and try to emulate it. In
    #your README file, explain the behavior you measure and illustrate in
    #the plot. The grader should be able to simply run your submitted program
    #and reproduce the plot.

    #If you want to be awesome (!), you can run each simulation
    #multiple times for each number of darts and calculate the standard
    #deviation for the execution time and the simulation rate, but this is not
    #required.

main()
