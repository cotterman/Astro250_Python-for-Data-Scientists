# Instructions: Write a module called CalCalc, with a method called "calculate" that evaluates any string passed to it,
# and can be used from either the command line (using argparse with reasonable flags) or imported within Python
# Feel free to use something like eval(), but be aware of some of the nasty things it can do, and make sure it doesn't have too much power:
# http://nedbatchelder.com/blog/201206/eval_really_is_dangerous.html


import sys
import argparse
import urllib #this allows me to read remote website as though it were a file
import urllib2 #this is a newer version of urllib
import httplib
from xml.dom.minidom import parseString #what I get thru W-A's API is an XML file
import xml.etree.ElementTree as ET #this may be a better alternative to minidom
import wolframalpha
import nose

################################################################

def get_command_lines():
    """
    Parse the info provided by user on command line
    """
    parser = argparse.ArgumentParser(description='User input to parse')
    parser.add_argument('mystring', help='This is the string to evaluate')
    parser.add_argument('-t', action='store_true', default=False,
                        dest='boolean_switch',
                        help='Set a switch to true')
    parser.add_argument('-f', action='store_false', default=False,
                        dest='boolean_switch',
                        help='Set a switch to false')
    return parser.parse_args()
    
def which_method(wolfram, mystring):
    """
    If user specifies to use Wolfram-Alpha, then use it
    Otherwise, use Python if possible
    """
    if wolfram==False:
        try:
            eval(mystring)
        except (TypeError, NameError, SyntaxError):
            wolfram = True
    return wolfram

def reformat(result):
    try:
        float(result)
    except (ValueError):
        return result
    else:
        return float(result)

def calculate(mystring, wolfram=False):
    """
    Evaluate mystring
    """
    if wolfram==False:
        try:
            eval(mystring)
        except (TypeError, NameError, SyntaxError):
            wolfram = True
        else:
            prelim =  eval(mystring)
    if wolfram==True:
        client = wolframalpha.Client("UY99YQ-8Y6WR5A3JQ")
        evaluation = client.query(mystring) 
        prelim = next(evaluation.results).text
    return reformat(prelim)

def calculate_with_wolfram():
    t = urllib.urlopen(url)
    t.read()

###########################################################################

def main():
    inputs = get_command_lines()
    w_method = which_method(inputs.boolean_switch, inputs.mystring)
    result = calculate(inputs.mystring, w_method)
    print 'The expression "' , inputs.mystring, '" evaluates to: \n', result
    print 'Evaluated using the Wolfram-Alpha API   =', w_method


#This if-statement says that if this script (CalCalc.py) is run directly, then execute main.  
    #Else, do not execute main (facilitates running "from CalCalc import calculate")
if __name__ == '__main__':
    main()


###########################################################################
#these tests will run when you type: nosetests CalCalc.py


def test_0():
    assert abs(4. - calculate("2**2")) < .001 #do not use wolfram-alpha unless necessary

def test_1():
    assert abs(4. - calculate("2**2", wolfram=True)) < .001 #use wolfram-alpha

def test_3():
    assert calculate("the date of thanksgiving")

def test_4():
    assert abs(9.8696 - calculate("pi^2")) < .001 #this one has trouble.  why?



