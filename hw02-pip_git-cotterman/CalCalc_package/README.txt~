
#########################################################################################

#A package is simply a directory with an __init__.py file inside it. For example:
    $ mkdir mypackage
    $ cd mypackage
    $ touch __init__.py
    $ echo "# A Package" > __init__.py
    $ cd ..
    #This creates a package that can be imported using the import. Example:
        >>> import mypackage #what good does this do??  I could not run calculate after importing my package

#The "setup.py" script will allow others to install my code into the Python path:
    $ python setup.py install

#I finished my package using distutils to create a standard, share-able zipped file:
    $ cd ~\my-python-seminar\hw02-pip_git-cotterman
    $ python setup.py sdist


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
