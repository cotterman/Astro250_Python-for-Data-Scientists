
###############################################################################
######################## Execution of my program ##############################
###############################################################################

My solution code is named "monte_carlo_parallelization.py"

#To use IPython for parallel computing (which I do), you need to start 
 one instance of the controller and one or more instances of the engine. 
#To start the IPython controller and 4 IPython engines, run this:
$ ipcluster start -n 4

You are now ready to run monte_carlo_parallelization.py in the usual fashion.

#after running the program, you should stop the engines via this command:
$ ipcluster stop

###############################################################################

RESULTS:
    #My program produces the graph "parallelization_results_v2.png"
        # _v1 is messed up b/c of problem with ax2.set_yscale('log')
            (I will ask about this during the next office hours) 
        # _v2 has scaling fixed by avoiding the set_yscale method altogether
    #When throwing few darts (<10,000), I find that no-parallelization
        is faster than both of the parallelization methods (lower execution times).  
    #When throwing more than 100,000 darts, the benefits of parallelization
        overwhelm the overhead of these methods, and they are about twice as fast
        as the simple serial method.
        This 2x speedup is as expected because my laptop has 2 separate cores
         (it advertises itself as having 4 cores, but effectively has just 2)
    #The simulation rate (darts per second) eventually converges for all methods
        as the overhead time becomes negligible.
    

My machine specifications:
    Operating system: Ubuntu 13.04
    Memory: 7.4 GiB
    Processor: Intel® Core™ i5-2450M CPU @ 2.50GHz × 4 


###############################################################################
######################## Stuff I learned ######################################
###############################################################################

#My notes on how multiprocessing code works are found in "example.py"

#Useful trick to obtain timing info for python program:
    will execute myprogram.py and provide real, user, and system run times:
    $ time python myprogram.py

#from within python, you can use the timeit.  For example:
>>> timeit 4+6
gives you the time it takes to calculate 4+6

#Not used for this assignment is a simple-to-use module called numexpr.
#Here is how to use it:
>>> import numpy as np
>>> import numexpr as ne
>>> a = np.arange (1 e6 )
>>> b = np.arange (1 e6 )
>>> ne.set _num_threads(4) #set number of threads to use
>>> ne.evaluate ( "a **2 + b **2 + 2* a * b" )
#the above line gives same result as (but in less time):
>>> a **2 + b **2 + 2* a * b
#check the time differences:
>>> timeit a **2 + b **2 + 2* a * b
>>> timeit ne.evaluate ( "a **2 + b **2 + 2* a * b" )

#starcluster is a tool that allows you to easily manage and 
 control Amazon machines from the command line.


###############################################################################
#################### Questions pertaining to this unit ########################
###############################################################################

(I'll come to office hours to ask about these next week)

#My graphed "simulation rates" are messed up in "parallelization_results_v1.png"
    It seems that ax2.set_yscale('log') scaled values for the simple simulation
     line, but not for the Icluster or multiprocessor lines.
    How can I fix this without actually scaling all numbers myself??

#See top of exper_ipython.py for quesitons regarding dview and map??


