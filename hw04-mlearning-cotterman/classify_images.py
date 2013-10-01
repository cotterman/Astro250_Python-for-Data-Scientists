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


def get_ppath():
    """
    Assume this script is in same folder as the "50_categories" folder
    and assume the "50_categories" folder contains images
    in folders labeled according to category (e.g., "camel", "airplane", etc.).
    """
    print ("\n This directory should contain script and folder of folders with images: ")
    ppath , file = os.path.split(os.path.realpath(__file__))
    print(ppath)
    return ppath

def get_categories(ppath, foldername):
    """
    Obtain list of categories, taken from folder titles.
    """
    categories = os.listdir(os.path.join(ppath, foldername)) 
    categories[:] = [c for c in categories if c != ".DS_Store"]
    return categories

def obtain_features(image):
    """
    Calculate image features, to be used as input for model.
    """
    
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

def summarize_trimages(categories, ppath, foldername):
    """
    For each image in training data, obtain image category and features list.
    """
    images_data = [] #create a list to contain summarized image data
    for category in categories:
        datapath = os.path.join(ppath, foldername, category)
        images_in_cat = os.listdir(datapath) #list of all image names in category
        for image_name in images_in_cat:
            image = misc.imread(datapath + "/" + image_name)
            image_features = obtain_features(image)
            image_features.append(category)
            images_data.append(image_features)
    return images_data

def summarize_vimages(ppath, foldername):
    """Obtain feature list for each image in validation set.
    
    """
    images_data = []
    datapath = os.path.join(ppath, foldername)
    validation_images = os.listdir(datapath) #list of validation image names
    validation_images.sort() #output will now be in more sensible order
    for image_name in validation_images:
        image = misc.imread(datapath + "/" + image_name)
        image_features = obtain_features(image)
        image_features.append(image_name)
        images_data.append(image_features)
    return images_data
        

def examine_images_data(images_data):
    """Examine content and type of data stored in images_data.
        
    """
    print "number of images: " , len(images_data) #4244 images
    print "#features: " , len(images_data[0]) - 1 #each image has Xx features + category name
    print "example of feature values: " , images_data[0] , "\n" #features and category for image 0


def random_guessing(Y, categories):
    """
    Calculate expected value of loss function if we guessed randomly.
    """
    print "Expected score (fraction of guesses that are correct)"
    print "if we guess each category with equal probability: " , \
            (float(len(Y))/len(categories))/len(Y) , "\n"


def feature_combos(images_data):
    nfeatures = len(images_data[0])-1
    feature_choices = [] #create a list of lists
    for i in xrange(nfeatures):
        f1 = i
        for j in xrange(i+1, nfeatures):
            f2 = j
            for k in xrange(j+1, nfeatures): 
                f3 = k
                feature_choices.append([f1, f2, f3])
    return feature_choices


def best_random_forest(X, Y, nfolds, parameters):
    """
    Fit "best" random forest by using parameters that minimize loss function 
    (i.e., maximize the score)
    """
    njobs = 1 #number of jobs to run in parallel -- pickle problems may occur if njobs > 1
    rf_tune = grid_search.GridSearchCV(RandomForestClassifier(), parameters,
                                       score_func=metrics.zero_one_score, n_jobs = njobs, cv = nfolds)
    return rf_tune.fit(X, Y)

def print_results(rf_opt):
    print("Grid of scores:\n" + str(rf_opt.grid_scores_) + "\n")
    print("Best zero-one score: " + str(rf_opt.best_score_) + "\n")
    print("Optimal Model:\n" + str(rf_opt.best_estimator_) + "\n")


def build_classifier(X, Y, nfolds, parameters):
    """
    Build classifier using "best" random forest.
    """
    print "here1"
    rf_opt = best_random_forest(X, Y, nfolds, parameters)
    print_results(rf_opt) #Results of the grid search for optimal random forest parameters.
    mypickledRF = open('RFClassifier' , 'wb') #w is for write; b is for binary
    pickle.dump(rf_opt.best_estimator_ , mypickledRF) #Save classifier in file "RFclassifier"
    mypickledRF.close()
    print "here2"

def best_feature_combo(images_data, X, Y, nfolds2, parameters2):
    """
    Find combination of features that produces highest score.
    """
    #make sure this list matches the one constructed in the obtain_features function
        #the order must also be identical
    feature_names = np.array(["meanR", "meanG", "meanB", "stdR", "stdG", "stdB"])
    feature_choices = feature_combos(images_data) #list of 3-feature options

    best_combo = [0,0,0]
    best_score = 0
    for fcombo in feature_choices:
        findices = np.array(fcombo)
        X2 = np.array([f[findices] for f in X]) #just the chosen features
        rf_opt = best_random_forest(X2, Y, nfolds2, parameters2)
        score = rf_opt.best_score_
        if score > best_score:
            best_score = score
            best_combo = fcombo
    
    print "Indices of most important 3 features: \n" , best_combo
    print "Names of the most important 3 features: \n" , feature_names[np.array(best_combo)]
    print "Score obtained using just these features: \n" , best_score


def print_predicted(vNames, vY_predicted):
    print "\n filename                   predicted_class            "
    print "------------------------------------------------------"
    for i in range(len(vNames)):
        print vNames[i] , "             " , vY_predicted[i]
    print "\n"


def run_final_classifier(vfolder):
    """
    Use the pickled classifier to classify validation images.
    Pickled classifier runs random forest using parameters
    deemed to be optimal from a cross-validated grid search
    with provided training images.
    """
    ppath , file = os.path.split(os.path.realpath(__file__))
    vimages_data = summarize_vimages(ppath, vfolder) #narray of images features
    vX = np.array([f[:-1] for f in vimages_data]) #just the features (X will be a list of lists)
    vNames = np.array([c[-1] for c in vimages_data]) #list of image names

    mypickledRF = open('RFClassifier' , 'rb') #r is for read; b is for binary
    clf = pickle.load(mypickledRF)
    vY_predicted = np.array(clf.predict(vX))

    print_predicted(vNames, vY_predicted)


###############################################################################

def main():
    
    ### Obtain image information (e.g., calculate features) ###
    ppath = get_ppath() #path of folder containing images
    foldername = "50_categories" #name of folder containing training images
    categories = get_categories(ppath, foldername) #list of image categories
    images_data = summarize_trimages(categories, ppath, foldername) #list of lists
    examine_images_data(images_data) #print basic info on what images_data contains
    X = np.array([f[:-1] for f in images_data]) #just the features (X will be a list of lists)
    Y = np.array([c[-1] for c in images_data]) #list of categories


    ### Calculate expected score if guessing category randomly#
    random_guessing(Y, categories)  


    ### Build classifier using "best" random forest ###
    nfolds = 3 #number of folds to use for cross-validation
    #n_estimators is number of trees in forest
    #max_features is the number of features to consider when looking for best split
    parameters = {'n_estimators':[5],  'max_features':[5]} # rf parameters to try
    build_classifier(X, Y, nfolds, parameters)


    ### Find the 3 most important features? Test 455 combos (455 = 15 choose 3) ###
    nfolds2 = 3
    parameters2 = {'n_estimators':[5]} # rf parameters to try
    best_feature_combo(images_data, X, Y, nfolds2, parameters2)


    ### Use the pickled classifier to classify validation images ###
    vfolder = "validation_images" #name of folder containing images to classify
    run_final_classifier(vfolder)

#This if-statement says that if this script (classify_images.py) is run directly, then execute main.  
    #Else, do not execute main (facilitates running "from classify_images import run_final_classifier")
if __name__ == '__main__':
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        main()

###############################################################################



