
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
from sklearn import grid_search
from sklearn import metrics

def get_ppath():
    """
    Assume this script is in same folder as the "50_categories" folder
    and assume the "50_categories" folder contains images
    in folders labeled according to category (e.g., "camel", "airplane", etc.).
    """
    print ("This directory should contain script and folder of folders with images: ")
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

def summarize_images(categories, ppath, foldername):
    """
    For each image, obtain image category and features list.
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

def examine_images_data(images_data):
    """
    Examine content and type of data stored in images_data.
    """
    print "type(images_data): ", type(images_data) #we have a list
    print "number of images: " , len(images_data) #4244 images
    print "#features: " , len(images_data[0]) - 1 #each image has Xx features + category name
    print "example of feature values: " , images_data[0] #list containing features and category for image 15


def random_guessing(Y, categories):
    """
    Calculate expected value of loss function if we guessed randomly.
    """
    print "Guess each category with equal probability: "
    print "    Expected score (fraction of guesses that are correct): " , (float(len(Y))/len(categories))/len(Y)


def feature_combos(images_data):
    nfeatures = len(images_data[0])-1
    feature_choices = [] #create a list of lists
    for i in range(nfeatures):
        f1 = i
        for j in range(i+1, nfeatures):
            f2 = j
            for k in range(j+1, nfeatures): 
                f3 = k
                feature_choices.append([f1, f2, f3])
    return feature_choices


def best_random_forest(X, Y, nfolds, parameters):
    """
    Fit "best" random forest by using parameters that minimize loss function 
    (i.e., maximize the score)
    """
    rf_tune = grid_search.GridSearchCV(RandomForestClassifier(), parameters,\
                                       score_func=metrics.accuracy_score, n_jobs = 2, cv = nfolds)
    return rf_tune.fit(X, Y)

def print_results(rf_opt):
    print("Grid of scores:\n" + str(rf_opt.grid_scores_) + "\n")
    print("Best zero-one score: " + str(rf_opt.best_score_) + "\n")
    print("Optimal Model:\n" + str(rf_opt.best_estimator_) + "\n")


def best_feature_combo(feature_choices, X, Y, nfolds2, parameters2):
    """
    Find combination of features that produces highest score.
    """
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
    print "Score obtained using just these features: \n" , best_score


###############################################################################

def main():
    
    #obtain image information (e.g., calculate features)

    ppath = get_ppath() #path of folder containing images
    foldername = "50_categories" #name of folder containing images
    categories = get_categories(ppath, foldername) #list of image categories
    images_data = summarize_images(categories, ppath, foldername) #list of lists
    examine_images_data(images_data) #print basic info on what images_data contains
    X = np.array([f[:-1] for f in images_data]) #just the features (X will be a list of lists)
    Y = np.array([c[-1] for c in images_data]) #list of categories

    random_guessing(Y, categories) #Expected score if guessing category randomly 


    #build classifier using "best" random forest

    nfolds = 3 #number of folds to use for cross-validation
    parameters = {'n_estimators':[50,100],  'max_features':[5,6]} # rf parameters to try
        #n_estimators is number of trees in forest
        #max_features is the number of features to consider when looking for best split
    rf_opt = best_random_forest(X, Y, nfolds, parameters)
    print_results(rf_opt) #Results of the grid search for optimal random forest parameters.


    #What are the 3 most important features? Test 455 combos (455 = 15 choose 3).
  
    feature_choices = feature_combos(images_data) #list of 3-feature options
    nfolds2 = 3
    parameters2 = {'n_estimators':[50,100]} # rf parameters to try
    best_feature_combo(feature_choices, X, Y, nfolds2, parameters2)
    
main()
 

###############################################################################



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
