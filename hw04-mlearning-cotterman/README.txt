
##############################################################################
##### Guide for running programs for hw04 ####################################
##############################################################################

#To successfully run my script, you should have the following folder structure:
    #You are running python from the directory that contains classify_images.py
    #Your pwd also contains a folder called "50_categories" which contains the 
        training data
    #Your pwd also contains a folder of images that you wish to classify
        This folder is called foldername_with_images_to_classify
        #note: you may use the folder in my repository, "validation_images"
    #Your pwd also contains the pickled classifier, "RFclassifier"

#To train the classifier (recreate RFclassifier) and classify validation images:
    $ python classify_images.py

#To classify validation set of images using my pickeled classifier:
    >>> from classify_images import run_final_classifier
    >>> run_final_classifier("foldername_with_images_to_classify")


##############################################################################
##### Some of the output from running classify_images.py #####################
##############################################################################


*** Features used for prediction ***

meanR :  Mean value of red channel.  (Or of single channel if only one color value)
meanG :  Mean value of green channel.  (Or of single channel if only one color value)
meanB :  Mean value of blue channel.  (Or of single channel if only one color value)
stdR :  Standard deviation of red channel.  (Or of single channel if only one color value)
stdG :  Standard deviation of green channel.  (Or of single channel if only one color value)
stdB :  Standard deviation of blue channel.  (Or of single channel if only one color value)


#CV score using the optimal random forest classifier: 
0.152686145146

#In comparison, the expected score from random guessing is:
1/50 = .02

#My 3 most important features: 
['meanG', 'stdR', 'stdB']


