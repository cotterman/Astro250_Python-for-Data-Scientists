
import numpy as np
import scipy as sp
import os  #has several functions for manipulating files and directories
import matplotlib.pyplot as plt
from scipy import ndimage
from scipy import misc
from scipy import stats
from scipy.ndimage import imread
import scipy.ndimage as ndi
from sklearn.ensemble import RandomForestClassifier
from sklearn import cross_validation
from sklearn.cross_validation import cross_val_score

def get_ppath():
    """
    Assume this script is in same folder as the "50_categories" folder
    and assume the "50_categories" folder contains images
    in folders labeled according to category (e.g., "camel", "airplane", etc.)
    """
    print ("This directory should contain script and folder of folders with images: ")
    ppath , file = os.path.split(os.path.realpath(__file__))
    print(ppath)
    return ppath

def get_categories(ppath, foldername):
    """
    Obtain list of categories, taken from folder titles
    """
    categories = os.listdir(os.path.join(ppath, foldername)) 
    categories[:] = [c for c in categories if c != ".DS_Store"]
    return categories

def obtain_features(image):
    
    #for color images
    if image.ndim>2:
        #Average of each of the channels (R, G, B)
        meanR = image[:,:,0].mean()
        meanG = image[:,:,1].mean()
        meanB = image[:,:,2].mean()
        #Standard deviation of each of the channels (R, G, B)
        stdR = image[:,:,0].std()
        stdG = image[:,:,1].std()
        stdB = image[:,:,2].std()
    #for black and white images
    else:
        meanR = image[:,:].mean()
        meanG = image[:,:].mean()
        meanB = image[:,:].mean()
        stdR = image[:,:].std()
        stdG = image[:,:].std()
        stdB = image[:,:].std()

    features = [meanR, meanG, meanB, stdR, stdG, stdB]
    return features

def summarize_images(categories, ppath, foldername):
    images_data = [] #create a list to contain summarized image data
    for category in categories:
        datapath = os.path.join(ppath, foldername, category)
        images_in_cat = os.listdir(datapath) #list of all image names in category
        for image_name in images_in_cat:
            image = misc.imread(datapath + "/" + image_name)
            #print image_name
            image_features = obtain_features(image)
            image_features.append(category)
            images_data.append(image_features)
    return images_data


###############################################################################

def main():
    
    ppath = get_ppath() #path of folder containing images
    foldername = "50_categories" #name of folder containing images
    categories = get_categories(ppath, foldername) #list of image categories
    print categories
    images_data = summarize_images(categories, ppath, foldername) #list of lists
    print type(images_data)
    print len(images_data) #4244 images
    #print len(images_data[15]) #each image has Xx features + category name
    print images_data[15] #list containing features and category for image 15
    
    #get inputs for random forest
    # training
    #train = 500
    #Xtr = digits['data'][:train]
    #Ytr = digits['target'][:train]
    #print("training size: " + str(len(Ytr)))
    # testing set
    #Xte = digits['data'][train:]
    #Yte = digits['target'][train:]
    #print("testing size: " + str(len(Yte)))

    #build classifier using 9/10 of data
    ntree = 10 #number of trees in the forest
    mtry = "sqrt" #number of features to consider when looking for best split
    rf1 = RandomForestClassifier(n_estimators=ntree, max_features=mtry)
     #   print rf1.feature_importances
    #rf1.fit(Xtr, Ytr)
    #test classifier using remaining 1/10
      #  preds = rf1.predict(Xte)
      #  print float(sum(preds!=Yte))/len(Yte)
    
main()
 

###############################################################################

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
