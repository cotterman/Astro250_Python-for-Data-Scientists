
###############################################################################
################################# Title: Data Analytics for Non-Profit ########
######### Author: Carolyn Cotterman ###########################################
###############################################################################

## Final code: "Watsi_data_analytics.py"
   (Other code in folder is scratch work and can be ignored.)


## Short Description:  Watsi (www.watsi.org) posts photos and descriptions of 
people in poor countries who are in need of a medical treatment that they 
cannot afford.  Each patient profile remains on the site until the patient’s 
treatment is fully funded by donors accessing the site.  Using Python’s webpage
parsing and machine-learning tools, I explore the determinants of donation 
rate. In particular, do patients who smile in their photo get funded more quickly?  


## Variable importance analysis for donation rate:

# Observational unit = patient

# Outcome measure = average dollars donated per day to patient

# Predictors and controls:
  Total cost of treatment
  Basic patient information:
    Age
    Gender*
    Region (Latin America vs. Asia vs. Africa)
  Photo attributes:
    Facial expression
  Time trend 
  Day-of-the-week
*Extracted from posted text (not provided directly)


############################# Employed lecture themes #########################

# Versioning (of course)
# Numpy & scipy 
# Plotting
# Pandas 
# sklearn
# Interacting with the world 


############################# Quick Summary of Results ########################
# results will be better presented on poster/ in person

# Older patients are more likely to smile, and less likely to get money quickly
# African patients are more likely to smile than are Asian and Latin American patients
# Random forest places facial expression as 3rd most important feature
    # most important is total cost of treatment, folowed by patient age 
# My linear regressions indicate smiling may be negatively correlated with donations
    # but most specifications gave high p-values for facial expression
    # all specifications suffer from problems with the linear model assumptions
# Inverse probability of treatment weighted (IPTW) results indicate smiling increases donations
    # Here, too, smiling does not appear significant




