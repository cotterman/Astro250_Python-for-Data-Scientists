
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
import math

import random
from random import uniform
from math import sqrt
from time import time

import multiprocessing
from multiprocessing import Pool, Process, Queue, Pipe

from IPython import parallel
from IPython.display import display


def simple_method(num_darts):
    """ Execute dart-throwing monte carlo with no parallelization
    """
    start_time = time()

    pi_approx = find_pi(num_darts)

    end_time = time()
    execution_time = end_time - start_time
    return execution_time

def darts_in_circle(num_darts):
    """Throw specified number of darts. Count number that fall in circle.
    """
    import random
    import math
    num_darts_in_circle = 0
    for n in xrange(num_darts):
        x, y = random.uniform(-1,1), random.uniform(-1,1)
        if math.sqrt(x**2 + y**2)<1:
            num_darts_in_circle +=1
    return num_darts_in_circle

def find_pi(num_darts): 
    """ Approximate pi by throwing num_darts
    """
    num_darts_in_circle = darts_in_circle(num_darts)
    pi_approx = ( num_darts_in_circle/float(num_darts) ) * 4
    return pi_approx


def do_parallel(num_darts_total):
    """Use ipython's parallel module to run monte carlo simulation.
    """
    start_time = time()

    rc = parallel.Client()
    dview = rc[:]
    nnod = len(dview) #number of engines (selected from commandline - see README)
    num_darts_divided =  math.trunc( float(num_darts_total) / nnod )

    #note syntax: nnod*[num_darts_divided] creates a list of length nnod with
        #each element having a value of num_darts_divided
    circle_total = sum( dview.map_sync(darts_in_circle, nnod*[num_darts_divided]) )

    #in case num_darts_total was not divisible by nnod, calculate darts thrown
    num_darts_total = num_darts_divided * nnod
    pi_approx = ( circle_total/float(num_darts_total) ) * 4
    
    end_time = time()
    execution_time = end_time - start_time
    return execution_time


def worker(input_queue, ip_queue_lock, output_queue, op_queue_lock):

    # loop until the queue is empty, and we can exit
    while True:
        # the lock is implicitly released when we exit from the with block
        with ip_queue_lock:
            # if there's nothing left to process, we're done,
            # so return from the worker function
            if len(input_queue) == 0: 
                return
            # get the arguments to pass to f
            num_darts = input_queue.pop()
        
        # outside of the lock, run f 
            #(we want different processes to be able to run f simultaneously)
        num_darts_in_circle = darts_in_circle(num_darts)
        with op_queue_lock:
            output_queue.append( num_darts_in_circle )

def do_multip(num_darts_total, NTHREADS):

    """Use python's multiprocessing module to run monte carlo simulation.
    """
    start_time = time()

    manager = multiprocessing.Manager()
    input_queue = manager.list()
    ip_queue_lock = multiprocessing.Lock()
    output_queue = manager.list()
    op_queue_lock = multiprocessing.Lock()

    #divide num_darts equally among processes
    num_darts_divided =  math.trunc( float(num_darts_total) / NTHREADS )
    remainder = num_darts_total % NTHREADS
    for i in xrange(NTHREADS):
        if i < NTHREADS - 1:
            input_queue.append(num_darts_divided)
        else:
            input_queue.append(num_darts_divided + remainder)
    #print "Total number of darts thrown: " , num_darts_total
    #print "Input queue: " , input_queue

    ps = []
    for i in xrange(NTHREADS):
        p = multiprocessing.Process(target=worker, args=(
            input_queue, ip_queue_lock, output_queue, op_queue_lock))
        p.start()
        ps.append( p )

    # wait for the children processes to terminate
    for p in ps: 
        p.join()
    #print "output list: " , output_queue

    #tally results from each process to find pi
    circle_total = 0
    for circle_count in output_queue:
        circle_total += circle_count
    pi_approx = ( circle_total/float(num_darts_total) ) * 4

    end_time = time()
    execution_time = end_time - start_time
    return execution_time


def make_plots(num_darts_list, execution_times_simple, execution_times_multip, execution_times_parallel):
    """Plot execution times for various runs
    """
    simulation_rates_simple = []
    simulation_rates_multip = []
    simulation_rates_parallel = []

    print "num_darts_list: " , num_darts_list
    print "length of num_darts_list: " , len(num_darts_list)

    for i in range(len(num_darts_list)):
        simulation_rates_simple.append( float(num_darts_list[i])/execution_times_simple[i] )
        simulation_rates_multip.append( float(num_darts_list[i])/execution_times_multip[i] )
        simulation_rates_parallel.append( float(num_darts_list[i])/execution_times_parallel[i] )

    print "simulation_rates_simple: " , simulation_rates_simple
    print "simulation_rates_multip: " , simulation_rates_multip
    print "simulation_rates_parallel: " , simulation_rates_parallel

    #manually switch everything to log scale
    lnum_darts_list = [math.log(x,10) for x in num_darts_list]
    lsimulation_rates_simple = [math.log(x,10) for x in simulation_rates_simple]
    lsimulation_rates_multip = [math.log(x,10) for x in simulation_rates_multip]
    lsimulation_rates_parallel = [math.log(x,10) for x in simulation_rates_parallel]
    lexecution_times_simple = [math.log(x,10) for x in execution_times_simple]
    lexecution_times_multip = [math.log(x,10) for x in execution_times_multip]
    lexecution_times_parallel = [math.log(x,10) for x in execution_times_parallel]

    f, ax = plt.subplots()
    lns1 = ax.plot(lnum_darts_list, lexecution_times_simple, 
                   label='Simple', color='r')
    lns2 = ax.plot(lnum_darts_list, lexecution_times_multip, 
                   label='Multiprocessing', color='c')
    lns3 = ax.plot(lnum_darts_list, lexecution_times_parallel,
                    label='IPcluster', color='g')

    ax2 = ax.twinx()
    lns4 = ax2.plot(lnum_darts_list, lsimulation_rates_simple, linestyle='--', 
                    color='r')
    lns5 = ax2.plot(lnum_darts_list, lsimulation_rates_multip, linestyle='--',
                    color='c')
    lns6 = ax2.plot(lnum_darts_list, lsimulation_rates_parallel, linestyle='--',
                    color='g')
                                   
    lns = lns1+lns2+lns3
    labs = [l.get_label() for l in lns]
    ax.legend(lns, labs, loc='lower right', frameon=False, fontsize='small')

    ax.set_title('Parallelization Performance', fontsize='x-large', fontname='serif', weight='semibold')
    ax.set_xlabel('log(Number of Darts)')
    ax.set_ylabel('log(Execution Times (seconds)), solid line')
    ax2.set_ylabel('log(Simulation Rates (darts per second)), dashed line')
    ax2.set_yticks(range(2,8))
    
    #this code caused problems, as it only scaled the simple method on secondary axis
    #ax.set_xlim(10,10000)
    #ax.set_xscale('log')
    #ax.set_yscale('log')
    #ax2.set_yscale('log')
    #ax2.set_ylim(10e1,10e6)

    plt.savefig('parallelization_results_v2.png')


def main():

    #Use a Monte Carlo dart-throwing simulation to calculate a 
    #numerical approximation to Pi withou parallelization. 

    #Run algorithm under different parallelization methods. 
    #Run several trials with different numbers of darts
    #thrown (up to execution times ~100 seconds). Keep track of the
    #execution times as a function of number of darts and method of
    #parallelization. Also, keep track of the simulation rate (darts thrown per
    #second). 

    num_darts_list = range(10,100,10)+\
                     range(100,1000,100)+\
                     range(1000,10000,1000)+\
                     range(int(1e4),int(1e5),int(1e4))+\
                     range(int(1e5),int(1e6),int(1e5))+\
                     [int(1e6),int(5e6),int(1e7)]

    #1) No parallelization

    execution_times_simple = []
    for num_darts in num_darts_list:
        execution_times_simple.append( simple_method(num_darts) )
    print "Execution times, no parallelization: " , execution_times_simple

    #2) Python multiprocessing (use the pool function). 

    execution_times_multip = []
    for num_darts in num_darts_list:
        execution_times_multip.append( do_multip(num_darts, NTHREADS=4) )
    print "Execution times, multiprocessing: " , execution_times_multip

    #3) IPython parallel 
    
    execution_times_parallel = []
    for num_darts in num_darts_list:
        execution_times_parallel.append( do_parallel(num_darts) )
    print "Execution times, ipython parallel: " , execution_times_parallel

    #Plot execution time and simulation rate as a function of number of darts
    #for all 3 methods. If you calculated std deviations, use errorbar plots.

    make_plots(num_darts_list, execution_times_simple, execution_times_multip, execution_times_parallel)

    #If you want to be awesome (!), you can run each simulation
    #multiple times for each number of darts and calculate the standard
    #deviation for the execution time and the simulation rate, but this is not
    #required.

main()
