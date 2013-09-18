

#distutils2: the standard way to take your directories of code 
    #and bundle them up for easy installation and use by others
#distutils2 is unavailable thru Ubuntu, so I will use the older version
from distutils.core import setup 

setup(name='CalCalc',
    version='0.01',
    license='LICENSE.txt',
    packages=['CalCalc']  #py_modules did not work here (for unknown reason)
    )

