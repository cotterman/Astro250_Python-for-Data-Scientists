
from numpy import *
from scipy import *
from scipy import signal

t = array([ [0,0,0,0],[0,5,10,0],[0,3,0,0] ])
g = array([ [10,2,0,0],[20,1,0,0],[0,0,0,0] ])

test3 = signal.fftconvolve(t,g)
test3
