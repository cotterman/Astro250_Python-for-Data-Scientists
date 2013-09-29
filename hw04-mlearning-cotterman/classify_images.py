
import numpy as np
import scipy as sp
import os  #The os.path module has several functions for manipulating files and directories
import matplotlib.pyplot as plt
from scipy import ndimage
from scipy import misc
from scipy import stats
from scipy.ndimage import imread
import scipy.ndimage as ndi


#Assume this script is in same folder as the "50_categories" folder
    #and assume the "50_categories" folder contains images
    #in folders labeled according to category (e.g., "camel", "airplane", etc.)
print ("Directory containing script and folder of folders: ")
ppath , file = os.path.split(os.path.realpath(__file__))
print(ppath)

#Obtain list of categories, taken from folder titles
foldername = "50_categories"
categories = os.listdir(os.path.join(ppath, foldername)) 
print categories

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
plt.imshow(image)
print type(image)

#Average of each of the channels (R, G, B)
meanR = image[:,:,0].mean()
meanG = image[:,:,1].mean()
meanB = image[:,:,2].mean()

#Standard deviation of each of the channels (R, G, B)
stdR = image[:,:,0].std()
stdG = image[:,:,1].std()
stdB = image[:,:,2].std()

features = [meanR, meanG, meanB, stdR, stdG, stdB]
print features

# Based on the feature set for each image, build a random forest classifier (scikits.learn).
#Produce metrics on your estimated error rates using cross-validation. How much better is this
#than the expectation with random guessing? What are the 3 most important features?


# Make sure your final classifier can run on a directory of different images, where a call like:
#   run_final_classifier("/new/directory/path/")
#  on directory that contains files like:
#    validation1.jpg
#    validation2.jpg 
#     ....
#  will produce an output file that looks like:
#    filename             predicted_class
#    ------------------------------------------
#    validation1.jpg          unicorn
#    validation2.jpg          camel
#     ....
