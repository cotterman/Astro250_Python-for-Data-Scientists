
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


def simple_method(num_darts):

    start_time = time()

    pi_approx = find_pi(num_darts)

    end_time = time()
    execution_time = end_time - start_time
    return execution_time

def darts_in_circle(num_darts):
    num_darts_in_circle = 0
    for n in xrange(num_darts):
        x, y = uniform(-1,1), uniform(-1,1)
        if sqrt(x**2 + y**2)<1:
            num_darts_in_circle +=1
    return num_darts_in_circle

def find_pi(num_darts): 
    """ Approximate pi by throwing num_darts
    """
    num_darts_in_circle = darts_in_circle(num_darts)
    pi_approx = ( num_darts_in_circle/float(num_darts) ) * 4
    return pi_approx


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
    print "Total number of darts thrown: " , num_darts_total
    print "Input queue: " , input_queue

    ps = []
    for i in xrange(NTHREADS):
        p = multiprocessing.Process(target=worker, args=(
            input_queue, ip_queue_lock, output_queue, op_queue_lock))
        p.start()
        ps.append( p )

    # wait for the children processes to terminate
    for p in ps: 
        p.join()

    print "output list: " , output_queue

    #tally results from each process to find pi
    circle_total = 0
    for circle_count in output_queue:
        circle_total += circle_count
    pi_approx = ( circle_total/float(num_darts_total) ) * 4
    print "Pi approximation: " , pi_approx

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
    #num_darts_list = [1000]

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
    execution_times_parallel = [10, 10, 10, 10, 10, 10]

    #Plot execution time and simulation rate as a function of number of darts
    #for all 3 methods. If you calculated std deviations, use errorbar plots.

    make_plots(num_darts_list, execution_times_simple, execution_times_multip, execution_times_parallel)

    #If you want to be awesome (!), you can run each simulation
    #multiple times for each number of darts and calculate the standard
    #deviation for the execution time and the simulation rate, but this is not
    #required.

main()
