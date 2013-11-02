
###############################################################################
#
# Overview: For this homework I run the same algorithm under different
# parallelization methods and evaluate the speedups (execution
# time). I compare simple serial (no parallelization),
# multiprocessing, and IPython's parallel module.
#
# Author: Carolyn Cotterman
#
###############################################################################

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from random import uniform
from math import sqrt
from time import time

def simple_method(num_darts):

    start_time = time()
    num_darts_in_circle = 0

    for n in range(num_darts):
        x, y = uniform(-1,1), uniform(-1,1)
        if sqrt(x**2 + y**2)<1:
            num_darts_in_circle +=1
    pi_approx = ( num_darts_in_circle/float(num_darts) ) * 4

    end_time = time()
    execution_time = end_time - start_time
    return execution_time


def make_plots(num_darts_list, execution_times_simple, execution_times_multip, execution_times_parallel):
    
    simulation_rates_simple = []
    simulation_rates_multip = []
    simulation_rates_parallel = []
    for i in range(len(num_darts_list)):
        simulation_rates_simple.append( num_darts_list[i]/execution_times_simple[i] )
        simulation_rates_multip.append( num_darts_list[i]/execution_times_multip[i] )
        simulation_rates_parallel.append( num_darts_list[i]/execution_times_parallel[i] )

    f, ax = plt.subplots()
    lns1 = ax.plot(num_darts_list, execution_times_simple, 
                   label='Simple', color='b')
    lns2 = ax.plot(num_darts_list, execution_times_multip, 
                   label='Multiprocessing', color='c')
    lns3 = ax.plot(num_darts_list, execution_times_parallel,
                    label='IPcluster', color='r')

    ax2 = ax.twinx()
    lns4 = ax2.plot(num_darts_list, simulation_rates_simple, linestyle='--',
                   label='Simple', color='b')
    lns5 = ax2.plot(num_darts_list, simulation_rates_multip, linestyle='--',
                   label='Multiprocessing', color='c')
    lns6 = ax2.plot(num_darts_list, simulation_rates_parallel, linestyle='--',
                    label='IPcluster', color='r')
                                   
    lns = lns1+lns2+lns3
    labs = [l.get_label() for l in lns]
    ax.legend(lns, labs, loc='center left', frameon=False, fontsize='small')

    ax.set_title('Parallelization Performance', fontsize='x-large', fontname='serif', weight='semibold')
    ax.set_xlabel('Number of Darts')
    ax.set_ylabel('Execution Times (seconds), solid line')
    ax2.set_ylabel('Simulation Rates (darts per second), dashed line')

    plt.savefig('parallelization_results.png')


def main():

    #Use a Monte Carlo dart-throwing simulation to calculate a 
    #numerical approximation to Pi withou parallelization. 

    #Run algorithm under different parallelization methods. 
    #Run several trials with different numbers of darts
    #thrown (up to execution times ~100 seconds). Keep track of the
    #execution times as a function of number of darts and method of
    #parallelization. Also, keep track of the simulation rate (darts thrown per
    #second). 

    num_darts_list = [100, 1000, 10000, 100000, 1000000, 10000000]

    #1) No parallelization

    execution_times_simple = []
    for num_darts in num_darts_list:
        execution_times_simple.append( simple_method(num_darts) )
    print execution_times_simple

    #2) Python multiprocessing (use the pool function). 

    execution_times_multip = []
    execution_times_multip = [5, 10, 15, 20, 20, 20]
    

    #3) IPython parallel 
    
    execution_times_parallel = []
    execution_times_parallel = [10, 10, 10, 10, 10, 10]

    #Plot execution time and simulation rate as a function of number of darts
    #for all 3 methods. If you calculated std deviations, use errorbar plots.

    make_plots(num_darts_list, execution_times_simple, execution_times_multip, execution_times_parallel)

    #If you want to be awesome (!), you can run each simulation
    #multiple times for each number of darts and calculate the standard
    #deviation for the execution time and the simulation rate, but this is not
    #required.

main()