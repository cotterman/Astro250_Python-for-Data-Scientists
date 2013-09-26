
************* Stuff learned from HW01 ########################


### working with ndarrays ###

print type(d) #we've got a numpy ndarray
print d.dtype #data is of type float
print d.ndim #2 dimensions (like a list of lists)
print d.shape #308 rows, 7 columns
print "col names: " , d.dtype.names #if the columns have names they will be printed here
print "the first 3 values of the first column: " , d[:3,0]
print "the first 3 values of the second column: ", d[:3,1]
print "the first 3 rows: ", d[:3,]
