
import os  #has several functions for manipulating files and directories
import pickle
import warnings

import numpy as np
import matplotlib.pyplot as plt

import scipy as sp
from scipy import ndimage
from scipy import misc
from scipy import stats
from scipy.ndimage import imread
import scipy.ndimage as ndi

from sklearn.ensemble import RandomForestClassifier
from sklearn import cross_validation
from sklearn.cross_validation import cross_val_score
from sklearn import grid_search
from sklearn import metrics

import skimage #must have installed yourself - not part of standard distribution
from skimage import feature


#Assume this script is in same folder as the "50_categories" folder
    #and assume the "50_categories" folder contains images
    #in folders labeled according to category (e.g., "camel", "airplane", etc.)
ppath = "/home/carolyn/my-python-seminar/hw04-mlearning-cotterman"


#Obtain list of categories, taken from folder titles
foldername = "50_categories"
categories = os.listdir(os.path.join(ppath, foldername)) 

#obtain images within each category
#for category in categories:
 #   if category != ".DS_Store": #would be cleaner to take this out of the "categories" list
  #      datapath = os.path.join(ppath, foldername, category)
   #     images_in_cat = os.listdir(datapath) #list of all image names in category
    #    for image_name in images_in_cat:
            #print image_name
            #image = misc.imread(datapath + "/" + image_name) 
    
# Write a set of methods that takes as input one of these images, and then computes real-numbered
#features as the return.  You should produce at least 15 features. 
category = "camel"
datapath = os.path.join(ppath, foldername, category)
image_name = str(category) + "_0001" + ".jpg"
image = misc.imread(datapath + "/" + image_name)


im2 = np.array([[0, 0, 1, 1],
                [0, 0, 1, 1],
                [0, 2, 2, 2],
                [2, 2, 3, 3]], dtype=np.uint8)


#Average of each of the channels (R, G, B)
meanR = image[:,:,0].mean()
meanG = image[:,:,1].mean()
meanB = image[:,:,2].mean()

#Standard deviation of each of the channels (R, G, B)
stdR = image[:,:,0].std()
stdG = image[:,:,1].std()
stdB = image[:,:,2].std()

basic_features = [meanR, meanG, meanB, stdR, stdG, stdB]
print basic_features



def get_textures(image):
    glcm = skimage.feature.greycomatrix(image, distances=[1], angles=[0], levels=256, symmetric=False, normed=False)
    contrast = skimage.feature.greycoprops(glcm, prop='contrast')[0][0]
    dissimilarity = skimage.feature.greycoprops(glcm, prop='dissimilarity')[0][0]
    homogeneity = skimage.feature.greycoprops(glcm, prop='homogeneity')[0][0]
    ASM = skimage.feature.greycoprops(glcm, prop='ASM')[0][0]
    return [contrast, dissimilarity, homogeneity, ASM]

if image.ndim>2:
    gray_textures = get_textures( np.dot(image[...,:3], [0.289, 0.577, 0.134]) )
    red_textures = get_textures( image[:,:,0] )
    green_textures = get_textures( image[:,:,1] )
    blue_textures = get_textures( image[:,:,2] )
    textures = gray_textures + red_textures + green_textures + blue_textures
else:
    gray_textures = get_textures( image )
    textures = gray_textures * 4

print textures

features = basic_features + textures
print features

    



    #corner detection
        #from skimage.feature import peak_local_max
        #first run median thresholding
        #then find 4 numbers using peak_local_max:
            #ratio of upper left-hand peak to total width of picture
            #ratio of upper right-hand peak to total width of picture
            #ratio of lower left-hand peak to total height of picture
            #ratio of lower right-hand peak to total height of picture

    #find coordinates of peak(s) -- distill to distance from top and distance from left side (2 numbers)
        #skimage.feature.peak_local_max(
            #image, min_distance=10, threshold_abs=0, threshold_rel=0.1, exclude_border=True, indices=True, num_peaks=inf, footprint=None, labels=None)





