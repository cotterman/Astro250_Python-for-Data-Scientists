
##############################################################################
##### Notes on using the CalCalc package #####################################
##############################################################################

#To install the CalCalc package:
    $ python setup.py install

#To run CalCalc from the command line:
    $ python CalCalc.py "3+18" 
    options:
        -f (default) says to run using python's eval function if possible
           use the Wolfram-Alpha API if necessary
        -t says to run using the Wolfram-Alpha API automatically

#To import the calculate function in Python:
    >>> from CalCalc import calculate
    >>> calculate("3+18")
    #note: the expression to evaluate should be enclosed in quotations



###############################################################################
##### Notes on the things I learned in completing this assignment #############
###############################################################################

#A package is simply a directory with an __init__.py file inside it. For example:
    $ mkdir mypackage
    $ cd mypackage
    $ touch __init__.py
    $ echo "# A Package" > __init__.py
    $ cd ..
    #This creates a package that can be imported using the import. 
    #Example:
        #lets say "mypackage" (which is a folder) contains code1.py and code2.py then
        >>> import mypackage.code1 #gives access to code1.py 
        >>> dir(mypackage.code1) #to view the methods available within code1.py
        >>> mypackage.code1.functionA(45) #to run FunctionA, with argument 45, which is contained in code1.py

#I finished my package using distutils to create a standard, share-able zipped file:
    $ cd ~/my-python-seminar/hw02-pip_git-cotterman/CalCalc_package
    $ python setup.py sdist

#The "setup.py" script will allow others to install my code into the Python path:
    $ python setup.py install


########################################################################################

#A virtual environment preserves a local "python egosystem" 
    so you can update python and its packages etc. but still run scripts using 
    a previously preserved state of the installation 
#Basic instructions for using a virual environment: 
    #To create virual environment called "ENV1" in your pwd:  
        $ virtualenv ENV1
        #This creates ENV1/lib/pythonX.X/site-packages, where any libraries you install will go.
    #If you create your virtual environment using the option "--system-site-packages", 
        then your virtual environment will inherit packages from /usr/lib/python2.7/site-packages 
        (or wherever your global site-packages directory is).  For example:
        $ virtualenv --system-site-packages ENV1
    #To activate the environment:
        $ source bin/activate
        #This will change your $PATH so its first entry is the virtualenv's bin/ directory. 
        #If you directly run a script or the python interpreter from the virtualenv's bin/ directory 
            (e.g. path/to/ENV1/bin/pip or /path/to/ENV1/bin/  python script.py) then there's no need for activation.
    #After activating an environment you can use the function deactivate to undo the changes to your $PATH.
        $ source deactivate
    #To remove environment:
        $ rm -r ENV1
#For additional info/instructions on virtual environments:: https://pypi.python.org/pypi/virtualenv

########################################################################################
