
###############################################################################
######### Title: Data Analytics for Maximizing Donations to Non-Profit ########
######### Author: Carolyn Cotterman ###########################################
###############################################################################

## Short Description:  Watsi (www.watsi.org) posts photos and descriptions of 
people in poor countries who are in need of a medical treatment that they 
cannot afford.  Each patient profile remains on the site until the patient’s 
treatment is fully funded by donors accessing the site.  Using Python’s image 
processing and machine-learning tools, I explore the determinants of donation 
rate. In particular, do patients who smile in their photo get funded more quickly?  


## Variable importance analysis for donation rate:

# Observational unit = patient

# Outcome measure = average dollars donated per day to patient

# Predictors:
  Medical information:
    Total cost of treatment
    Type of medical issue: cosmetic vs. physical disability vs. life-threatening*
    whether medical issue resulted from accident vs. biologically developed*
  Basic patient information
    Age
    Gender*
    Marital status*
    Parenthood status*
    Region (Latin America vs. Asia vs. Africa)
  Photo attributes (size of face in frame, outdoor/indoor, smile/serious, focal point of eyes)
  Text description (number of characters, mention of career ambitions.)

# Controls:
  Number of other profiles posted on site at the same time
  Time trend 
  Seasonal trend 
  Day-of-the-week
*Extracted from posted text (not provided directly)


############################# Employed lecture themes #########################

# Versioning (of course)
# Numpy & scipy 
# Plotting
# Pandas 
# Interacting with the world 


