

#distutils2: the standard way to take your directories of code and bundle them up for easy installation and use by others
from distutils.core import setup #distutils2 is unavailable thru Ubuntu, so I will use this version

setup(name='CalCalc',
    version='0.01',
    license='LICENSE.txt',
    packages=['CalCalc']  #this would instead be py_modules if I were using distutils2
    )

