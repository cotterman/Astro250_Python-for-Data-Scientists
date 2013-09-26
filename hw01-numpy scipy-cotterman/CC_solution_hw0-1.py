import numpy as np
import scipy as sp
from scipy import ndimage
from scipy import misc
from scipy.ndimage import imread

dir = "/home/carolyn/python-seminar/Homeworks/hw_0_cotterman/Data/"
 
 
def read_originals():
    """
    read in the images (will create ndarrays called im_a thru im_e)
    """
    images = [] #place images in this list
    for myim in ["a","b","c","d","e"]:
        image = misc.imread(dir+"im1-"+myim+".png") 
        images.append(image)
    return images


def find_dot(image):  
    """
    find where the pigment is lightest
    """
    pigmin = image.min() #pigment at location of dot (unless colors are reversed?)
    for x in xrange(image.shape[0]): #xrange works just as well as range but does not generate the list in memory
        for y in xrange(image.shape[1]):
            if image[x,y,0] == pigmin: 
                return x, y #will return first pixal meeting criterial (upper-left most)


def get_offsets(dot_locate):
    """
    find the offset of the other images with respect to the first image
    """
    shifts = [] #to contain list of 4 couples
    for myim in dot_locate[1:]:
        xshift = dot_locate[0][0] - myim[0]
        yshift = dot_locate[0][1] - myim[1]
        shift = (xshift, yshift)
        shifts.append(shift)
    return shifts


def shift_images(images, shifts):
    """
    align the images.  
       save images in numpy arrays (for the next part) 
       also save images as .png files, appropriately named
    """
    counter = 0
    shifted_arrays = [] #this will contain the shifted images
    for label, myim in zip("bcde", images[1:]):
        xshift = shifts[counter][0]
        yshift = shifts[counter][1]
        narray_shift = sp.ndimage.interpolation.shift(input=myim, shift=(xshift, yshift,0) )
        shifted_arrays.append(narray_shift)
        misc.imsave(dir+"im1-"+label+"-shift.png", narray_shift)
        counter += 1
    return shifted_arrays

def mask_arrays(shifted_arrays):
    """
    create a mask for pixals with value [183 183 183 255] and [0 0 0 255]
    """
    masked_arrays = []
    for myarray in shifted_arrays:
        mymask = np.zeros(myarray.shape, dtype=int)
        for x in xrange(myarray.shape[0]): 
            for y in xrange(myarray.shape[1]):
                if myarray[x,y,0] == 183 or myarray[x,y,0] == 0:
                    mymask[x,y,] = [1,1,1,1]            
        mymasked = np.ma.masked_array(myarray, mask=mymask)
        masked_arrays.append(mymasked)    
    return masked_arrays

def combine_images(masked_arrays):
    """
    Combine the masked arrays using np.ma.median to reveal the hidden message
    Save combined image as png file
    """
    masked_arrays_array = np.ma.masked_array(masked_arrays)  
    combined = array(np.ma.median(masked_arrays_array, axis=0), dtype=uint8)
    imshow(combined,cmap=cm.Greys) #I think the word is Heisenberg    
    combined2 = array(np.ma.mean(masked_arrays_array, axis=0), dtype=uint8) #this looks better
    imshow(combined2,cmap=cm.Greys) #The word is Heisenberg
    misc.imsave(dir+'combined_image_v1.png', combined2) #save image as png file    


#####################################################################

def main():
    
    #STEP 1: find the location of the center of the black dot in all five images 
    #and report those locations as a list of 5 tuples
    images = read_originals()
    dot_locate = [] #this list will store location of dots
    for myim in images:
        dot_locate.append(find_dot(myim))
    print dot_locate
    
    #STEP 2: Using the location of the black dot in the first image, 
    #find the offset of the other images with respect to the first image. 
    #perform a shift on the other four images such that they are "registered" (aligned) 
    #with the first image.  
    shifts = get_offsets(dot_locate)
    shifted_arrays = shift_images(images, shifts)
    
    #STEP 3: Mask out the registered images by finding an appropriate mask 
    #for the grey-level regions making 5 new masked arrays.
    #Combine the masked arrays using np.ma.median to reveal the hidden message.
    masked_arrays = mask_arrays(shifted_arrays)
    combine_images(masked_arrays)
        
main()
