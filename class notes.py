
### Lecture 2 ###

import numpy as np
import scipy as sc
import numexpr as ne
#ne.evaluate uses multiple threads and does not save intermediate values like just doing a**2 + b**2 + 2*a*b would

##Broadcasting
#rules are complicated -- read and play on your own
#broadcasting is efficient, as it does not write full matrices to memory

##Stoichiometry example
#never want to solve a linear algebra problem by taking an inverse
#inverses are often very difficult to compute and might be close to zero, which breaks many algorithms
#so find a psuedo-inverse as demonstrated (np.linalg.solve)

##random sampling
#axis indicates along which dimension you want to find the statistic (row or column etc.)

##Masks
#where mask is true, the data is invalid (not counted in operations).  Useful for missing data.

##Breakout session

#create deck shell
deck_desc = [('suit', (np.string_, 9)), ('card', (np.string_, 1)), ('value', np.int32)]
deck = np.zeros(52, dtype=deck_desc)
print deck

#fill deck with values
mycards_in_suit = ['A','1','2','3','4','5','6','7','8','9','10','J','Q','K']
mysuits = ['hearts','spades','diamonds','clubs']
values = {
counter = 0
for suit in mysuits:
    for card in mycards_in_suit:
        value = 
        deck[counter] = (suit,card,value)         

##scipy tends to be more efficient than numpy
    #note: scipy requires a bunch of machinery to run (e.g., fortran libraries), so sometime you may want numpy

