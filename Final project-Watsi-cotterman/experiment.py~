

import os
import re
import numpy as np
import pandas as pd
import urllib2
from datetime import datetime
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf

from sklearn.ensemble import RandomForestRegressor
from sklearn import cross_validation
from sklearn.cross_validation import cross_val_score
from sklearn import grid_search
from sklearn import metrics

import skimage #must have installed yourself - not part of standard distribution
from skimage import feature

###############################################################################

#folders within folder from which code is run
downloadfolder = "/Watsi_data_downloaded/"
processedfolder = "/Watsi_data_processed/"
resultsfolder = "/Summary_plots_and_tables/"
ppath = os.getcwd()

#file containing main data of interest
towrite = "Data_summary.csv" 
towrite_path = ppath + processedfolder + towrite

###############################################################################

def read_data_csv():

    mydf = pd.read_csv(towrite_path)

    #want to make sure dates come in as dates
    mydf['date_posted'] = pd.to_datetime(mydf['date_posted'])
    mydf['date_funded'] = pd.to_datetime(mydf['date_funded'])

    return mydf


def main():

    ## Read in csv and correct formating that was lost in transition
    mydf = read_data_csv()

    #eliminate rows that have 1 or more missing values
    mydf = mydf.dropna(axis=0)
    #convert region to something numerical
    numeric_regions = {
        'Africa': 1,
        'Asia': 2,
        'Central America/ Caribbean': 3,
    }
    mydf['region_num'] = mydf['region'].map(numeric_regions)
    
    ###

    predictor_names = ['week_day_num_posted','day_posted','maleness','region_num', \
                      'treat_cost','patient_age','smile_scale']
    numfeat = len(predictor_names)
    Y = mydf.dollars_per_day #variable to predict
    X = mydf[predictor_names]
    
    #Build classifier using "best" random forest
    nfolds = 3 #number of folds to use for cross-validation
    #n_estimators is number of trees in forest
    #max_features is the number of features to consider when looking for best split
    parameters = {'n_estimators':[10,100,1000],  'max_features':[3,5,7]} # rf parameters to try
    njobs = 1 #number of jobs to run in parallel -- pickle problems may occur if njobs > 1
    rf_tune = grid_search.GridSearchCV(RandomForestRegressor(), parameters,
                             n_jobs = njobs, cv = nfolds)
    rf_opt = rf_tune.fit(X,Y)
    
    #Results of the grid search for optimal random forest parameters.
    print("Grid of scores:\n" + str(rf_opt.grid_scores_) + "\n")
    print("Best zero-one score: " + str(rf_opt.best_score_) + "\n")
    print("Optimal Model:\n" + str(rf_opt.best_estimator_) + "\n")
    #print "Parameters of random forest:\n " , rf_opt.get_params()

    #save optimal random forest regressor for future
    #mypickledRF = open('RF_Regressor' , 'wb') #w is for write; b is for binary
    #pickle.dump(rf_opt.best_estimator_ , mypickledRF) #Save classifier in file "RFclassifier"
    #mypickledRF.close()

    #Now use the optimal model's parameters to run random forest
        #(I couldn't get feature importances directly from the GridSearchCV fit)
    crf = RandomForestRegressor(n_jobs=njobs, max_features=3, n_estimators=1000).fit(X,Y) 
    print "Parameters used in chosen RF model:\n " , crf.get_params()

    plotting_names = np.array(('Day','Date','Sex','Region','Cost','Age','Smile'))
    print crf.feature_importances_
    indices = np.argsort(crf.feature_importances_)[::-1][:numfeat]
    plt.bar(xrange(numfeat), crf.feature_importances_[indices], align='center', alpha=.5)
    plt.xticks(xrange(numfeat), plotting_names[indices], rotation='horizontal', fontsize=12)
    plt.xlim([-1, numfeat])
    plt.ylabel('Feature importances', fontsize=12)
    plt.title('Feature importances computed by Random Forest', fontsize=16)
    plt.savefig('03_feature_importance.png', dpi=150);

main()




