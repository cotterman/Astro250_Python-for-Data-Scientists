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


def get_ppath():
    """Obtain path of folder in which this script is located.

    Assume this script is in same folder as the "50_categories" folder
    and assume the "50_categories" folder contains images
    in folders labeled according to category (e.g., "camel", "airplane", etc.).
    """
    print ("\n This directory should contain script and folder of folders with images: ")
    ppath , file = os.path.split(os.path.realpath(__file__))
    print(ppath)
    return ppath


def get_categories(ppath, foldername):
    """Obtain list of categories, taken from folder titles.

    """
    categories = os.listdir(os.path.join(ppath, foldername)) 
    categories[:] = [c for c in categories if c != ".DS_Store"]
    return categories


def get_basic_features(image):
    """Obtain easily/quikley calculated features.

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

    return [meanR, meanG, meanB, stdR, stdG, stdB]


def get_textures(image):
    """ Find the grey-level co-occurence matrix (GLCM) and summarize its properties.

    """
    #Calculate the grey-level co-occurrence matrix (GLCM).
    glcm = skimage.feature.greycomatrix(image, distances=[1], angles=[0], levels=256, symmetric=False, normed=False)

    #Calculate texture properties of a GLCM.
    contrast = skimage.feature.greycoprops(glcm, prop='contrast')[0][0]
    dissimilarity = skimage.feature.greycoprops(glcm, prop='dissimilarity')[0][0]
    homogeneity = skimage.feature.greycoprops(glcm, prop='homogeneity')[0][0]
    ASM = skimage.feature.greycoprops(glcm, prop='ASM')[0][0]

    return [contrast, dissimilarity, homogeneity, ASM]


def obtain_features(image):
    """Calculate image features, to be used as input for model.

    """
    basic_features = get_basic_features(image)

    if image.ndim>2:
        grey_textures = get_textures( np.dot(image[...,:3], [0.289, 0.577, 0.134]) )
        red_textures = get_textures( image[:,:,0] )
        green_textures = get_textures( image[:,:,1] )
        blue_textures = get_textures( image[:,:,2] )
        textures = grey_textures + red_textures + green_textures + blue_textures
    else:
        grey_textures = get_textures( image )
        textures = grey_textures * 4

    return basic_features + textures


def feature_descriptions(feature_names, printme):
    """ Create dictionary containing feature descriptions.  And print features used (optional).

    """
    features_desc = {
        'meanR': "Mean value of red channel.  (Or of single channel if only one color value)",
        'meanG': "Mean value of green channel.  (Or of single channel if only one color value)",
        'meanB': "Mean value of blue channel.  (Or of single channel if only one color value)",
        'stdR':  "Standard deviation of red channel.  (Or of single channel if only one color value)",
        'stdG':  "Standard deviation of green channel.  (Or of single channel if only one color value)",
        'stdB':  "Standard deviation of blue channel.  (Or of single channel if only one color value)",

        'grey_contrast': "grey contrast, based on the grey co-occurrence matrix using skimage.feature",
        'grey_dissimilarity': "grey dissimilarity, based on the grey co-occurrence matrix using skimage.feature",
        'grey_homogeneity': "grey homogeneity, based on the grey co-occurrence matrix using skimage.feature",
        'grey_ASM': "grey ASM, based on the grey co-occurrence matrix using skimage.feature",

        'red_contrast': "red contrast, based on the red co-occurrence matrix using skimage.feature",
        'red_dissimilarity': "red dissimilarity, based on the red co-occurrence matrix using skimage.feature",
        'red_homogeneity': "red homogeneity, based on the red co-occurrence matrix using skimage.feature",
        'red_ASM': "red ASM, based on the red co-occurrence matrix using skimage.feature",

        'green_contrast': "green contrast, based on the green co-occurrence matrix using skimage.feature",
        'green_dissimilarity': "green dissimilarity, based on the green co-occurrence matrix using skimage.feature",
        'green_homogeneity': "green homogeneity, based on the green co-occurrence matrix using skimage.feature",
        'green_ASM': "green ASM, based on the green co-occurrence matrix using skimage.feature",

        'blue_contrast': "blue contrast, based on the blue co-occurrence matrix using skimage.feature",
        'blue_dissimilarity': "blue dissimilarity, based on the blue co-occurrence matrix using skimage.feature",
        'blue_homogeneity': "blue homogeneity, based on the blue co-occurrence matrix using skimage.feature",
        'blue_ASM': "blue ASM, based on the blue co-occurrence matrix using skimage.feature"
        }

    if printme==True:
        print "*** Features used for prediction ***"
        for feature in feature_names:
            print feature , ": " , features_desc[feature]
    print "\n"


def summarize_trimages(categories, ppath, foldername):
    """For each image in training data, obtain image category and features list.

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
    """Calculate expected value of loss function if we guessed randomly.

    """
    print "Expected score (fraction of guesses that are correct)"
    print "if we guess each category with equal probability: " , \
            (float(len(Y))/len(categories))/len(Y) , "\n"


def feature_combos(images_data):
    """ Find all 3-feature combos in the feature space.

    """
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
    """Fit "best" random forest by using parameters that minimize loss function 

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
    """Build classifier using "best" random forest.

    """
    rf_opt = best_random_forest(X, Y, nfolds, parameters)
    print_results(rf_opt) #Results of the grid search for optimal random forest parameters.
    mypickledRF = open('RFClassifier' , 'wb') #w is for write; b is for binary
    pickle.dump(rf_opt.best_estimator_ , mypickledRF) #Save classifier in file "RFclassifier"
    mypickledRF.close()


def best_feature_combo(images_data, X, Y, nfolds2, parameters2, feature_names):
    """Find combination of features that produces highest score.

    """
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
    
    print "Names of the most important 3 features: \n" , [feature_names[i] for i in best_combo]
    print "Score obtained using just these features: \n" , best_score


def print_predicted(vNames, vY_predicted):
    print "\n filename                   predicted_class            "
    print "------------------------------------------------------"
    for i in range(len(vNames)):
        print vNames[i] , "             " , vY_predicted[i]
    print "\n"


def run_final_classifier(vfolder):
    """Use the pickled classifier to classify validation images.

    Pickled classifier runs random forest using parameters
    deemed to be optimal from a cross-validated grid search
    with provided training images.
    """
    ppath , file = os.path.split(os.path.realpath(__file__))
    #vimages_data = summarize_vimages(ppath, vfolder) #narray of images features
    #vX = np.array([f[:-1] for f in vimages_data]) #just the features (X will be a list of lists)
    #vNames = np.array([c[-1] for c in vimages_data]) #list of image names

    mypickledRF = open('RFClassifier' , 'rb') #r is for read; b is for binary
    clf = pickle.load(mypickledRF)
    print clf.feature_importances_.shape

    numfeat = 6
    indices = np.argsort(clf.feature_importances_)[::-1][:numfeat]
    plt.bar(xrange(numfeat), clf.feature_importances_[indices], align='center', alpha=.5)
    #plt.xticks(xrange(numfeat), X.columns[indices], rotation='vertical', fontsize=12)
    plt.xlim([-1, numfeat])

    plt.ylabel('Feature importances', fontsize=12)

    #plt.suptitle('Feature importances computed by Random Forest', fontsize=16)

    #f = gcf()
    #subplots_adjust(bottom=0.3)
    #f.set_size_inches(11, 8);
    plt.savefig('feature_importance.png', dpi=150);

    #vY_predicted = np.array(clf.predict(vX))
    #print_predicted(vNames, vY_predicted)


###############################################################################

def main():
    
    ### Obtain image information (e.g., calculate features) ###
    ppath = get_ppath() #path of folder containing images
    foldername = "50_categories" #name of folder containing training images
    categories = get_categories(ppath, foldername) #list of image categories
    #images_data = summarize_trimages(categories, ppath, foldername) #list of lists
    #examine_images_data(images_data) #print basic info on what images_data contains
    #X = np.array([f[:-1] for f in images_data]) #just the features (X will be a list of lists)
    #Y = np.array([c[-1] for c in images_data]) #list of categories


    #make sure this list matches the one constructed in the obtain_features function
    #the order must also be identical
    feature_names = ["meanR", "meanG", "meanB", "stdR", "stdG", "stdB", 
        "grey_contrast", "grey_dissimilarity", "grey_homogeneity", "grey_ASM",
        "red_contrast", "red_dissimilarity", "red_homogeneity", "red_ASM",
        "green_contrast", "green_dissimilarity", "green_homogeneity", "green_ASM",
        "blue_contrast", "blue_dissimilarity", "blue_homogeneity", "blue_ASM"] #features used
    #feature_descriptions(feature_names, printme=True) #print features and their descriptions


    ### Calculate expected score if guessing category randomly#
    #random_guessing(Y, categories)  


    ### Build classifier using "best" random forest ###
    nfolds = 3 #number of folds to use for cross-validation
    #n_estimators is number of trees in forest
    #max_features is the number of features to consider when looking for best split
    parameters = {'n_estimators':[5,10],  'max_features':[5,7,10]} # rf parameters to try
    #build_classifier(X, Y, nfolds, parameters)


    ### Find the 3 most important features? Test 455 combos (455 = 15 choose 3) ###
    #nfolds2 = 3
    #parameters2 = {'n_estimators':[5, 100]} # rf parameters to try
    #best_feature_combo(images_data, X, Y, nfolds2, parameters2, feature_names)


    ### Use the pickled classifier to classify validation images ###
    vfolder = "validation_images" #name of folder containing images to classify
    run_final_classifier(vfolder)


###############################################################################

#This if-statement says that if this script (classify_images.py) is run directly, then execute main.  
    #Else, do not execute main (facilitates running "from classify_images import run_final_classifier")
if __name__ == '__main__':
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        main()

###############################################################################



