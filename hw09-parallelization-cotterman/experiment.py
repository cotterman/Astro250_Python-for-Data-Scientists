

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from random import uniform
from math import sqrt
from time import time

from multiprocessing import Pool, Process, Queue, Pipe


def g(name):
    print 'hello', name

def do_multi():

    #p = Pool(5)
    #def f(x):
    #    return x*x
    #p.map(f, [1,2,3])

    #spawn a process
    p = Process(target=g, args=('Boley',))
    p.start()
    p.join() #what does this do??

    pool = Pool(processes=4)              # start 4 worker processes
    result = pool.apply_async(g, [10])    # evaluate "f(10)" asynchronously
    print result.get(timeout=1)           # prints "100" unless your computer is *very* slow
    print pool.map(g, range(10))          # runs function g with values "[0, 1, 4,..., 9]"

    #spawn a process and get result using the queue class
    def f(q):
        q.put([42, None, 'hello'])
    q = Queue()
    p = Process(target=f, args=(q,))
    p.start()
    print q.get()  # prints "[42, None, 'hello']"
    p.join()

    #Each connection object has send() and recv() methods (among others). 
        #Data in a pipe may become corrupted if two processes (or threads) 
            #try to read from or write to the same end of the pipe at the same time. 
        #No risk of corruption from processes using diff ends of same pipe at same time.
    def f(conn):
        conn.send([800, "Nathan", 'hello'])
        conn.close()
    parent_conn, child_conn = Pipe() #returns pair of objects connected by a pipe
    p = Process(target=f, args=(child_conn,))
    p.start()
    print parent_conn.recv()   # prints "[800, "Nathan", 'hello']"
    p.join()


def main():
    
    do_multi()

main()

