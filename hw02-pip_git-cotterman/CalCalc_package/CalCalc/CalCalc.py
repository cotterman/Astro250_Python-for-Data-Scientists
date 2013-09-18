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
    if type(result)==str and result[-3:]=="...":
        result = result[:-3] #eliminate the ... at the end
    try:
        float(result)
    except (ValueError):
        return result
    else:
        return float(result)  

def getOutpage(myinput):
    query = {"input": myinput, "appid": "UAGAWR-3X6Y8W777Q", "format": "plaintext"}
    return urllib2.urlopen("http://api.wolframalpha.com/v2/query?{}".format(urllib.urlencode(query)))

def getWAsolution(myinput):
    outpage = getOutpage(myinput)
    tree = ET.parse(outpage)
    root = tree.getroot()
    for pod in root: #iterate thru the "pods"
        try: #not all pods have titles and we do not want to get error
            pod.attrib['title']
        except KeyError: 
            continue #skip over the pods without titles
        
        if pod.attrib['title']=='Result' or pod.attrib['title']=='Exact result' or pod.attrib['title']=='Decimal form':
            prelim = pod[0][0].text
        if pod.attrib['title']=='Decimal approximation':
            prelim = pod[0][0].text

    return reformat(prelim)

def calculate(mystring, wolfram=False):
    """
    Evaluate mystring
    """
    if type(mystring)!=str:
        raise ValueError, "expression to evaluate must be enclosed in quotations"
    if wolfram==False:
        try:
            eval(mystring)
        except (TypeError, NameError, SyntaxError):
            wolfram = True
        else:
            prelim =  eval(mystring)
            return reformat(prelim)
    if wolfram==True: 
        return getWAsolution(mystring)
   

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
#these tests will run from terminal by typing: $ nosetests CalCalc.py


def test_1():
    assert abs(4. - calculate("2**2")) < .001 #do not use wolfram-alpha unless necessary

def test_2():
    assert abs(4. - calculate("2**2", wolfram=True)) < .001 #use wolfram-alpha

def test_3():
    assert calculate("the date of thanksgiving")

def test_4():
    assert abs(9.8696 - calculate("pi^2")) < .001 

def test_5():
    assert abs(0.09090909 - calculate("2. / 22", wolfram=True)) < .001

def test_6():
    assert abs(0.09090909 - calculate("2. / 22", wolfram=False)) < .001



