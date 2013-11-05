
#Before running this code, you must start the IPython controller and IPython engines:
#$ ipcluster start -n 4 
#(above line will start 4 clients)

### Question: what is the differenct between doing 
    #view = rc.load_balanced_view()
    #print view.map(mul, range(1,10), range(2,11))
#vs
    #dview = rc[:]
    #print dview.map(mul, range(1,10), range(2,11))
#??  Also, is dview.map short for dview.map_sync or are they different?
    #(And I thought that rc.block = True determined sync/async...
        #...does specifying map_sync/map)async override the rc.block value?)

###############################################################################

import os, sys, time
from IPython import parallel
import numpy as np

rc = parallel.Client()
print rc
print rc.ids #[0,1,2,3]


#a simple function
def mul(a,b):
    return a*b
print mul(5,6)

###############################################################################

#Synchronous execution:

rc.block = True

#call this function remotely
print rc[0].apply(mul, 5, 6)

#run in parallel
print rc[:].apply(mul, 5, 6)

#map is a python built-in used to run a function with a variety of arguments
print map(mul, range(1,10), range(2,11))

#execute in parallel
view = rc.load_balanced_view()
print view.map(mul, range(1,10), range(2,11))

###############################################################################

#Asynchronous execution:

rc.block = False

print rc[:].apply(mul,5,6).get() #.get() will fetch the answer

view = rc.load_balanced_view()
print view.map(mul, range(1,10), range(2,11)).get()


###############################################################################

#scatter and gather: 

#Lots of parallel computations involve partitioning data onto processes.
#DirectViews have scatter() and gather() methods, to help with this. 
#Pass any container or numpy array, and IPython will partition the object onto 
  #the engines wih scatter, or reconstruct the full object in the Client with gather().

dview = rc[:]
#its kind of weird (to me), but dview is not the same thing as rc:
    #( slicing can change the object type even if you take [:] )
print "print rc: " , rc  #this is a parallel client object
print "print dview: " , dview #this is a "direct view"
dview.block = True

dview.scatter('a',np.arange(16))
a = len(dview['a'])

print 'a in the engines:', dview['a']
print 'a here:', a
print 'len of whole thing:', len(dview.gather('a'))

dview.execute("asum = sum(a)") #each engine will find sum(a) for the a assigned to them
dview.gather('asum') #results from each engine as a list

######################

#DirectViews have a map method, which behaves just like the builtin map, but computed in parallel.

dview.block = True

serial_result   =       map(lambda x:x**10, range(32))
parallel_result = dview.map(lambda x:x**10, range(32))
async_result    = dview.map_async(lambda x:x**10, range(32)).get()
sync_result     = dview.map_sync(lambda x:x**10, range(32))

print "serial_result: \n" , serial_result
print "parallel_result: \n" , parallel_result
print "async_result: \n" , async_result
print "sync_result: \n" , sync_result

print serial_result==parallel_result #true
print async_result==parallel_result #true
print async_result==sync_result #true





