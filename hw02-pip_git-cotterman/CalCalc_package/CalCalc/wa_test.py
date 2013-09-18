#figure out how to use wolfa-alpha's API

import sys
import argparse
import urllib #this allows me to read remote website as though it were a file
import urllib2 #this is a newer version of urllib
import httplib
from xml.dom.minidom import parseString 
import xml.etree.ElementTree as ET #this may be a better alternative to minidom:
    #(from stackoverload:) "ElementTree needs much less memory for XML trees than DOM (and thus is faster)"
import wolframalpha


#2+15 --> 2%2B15
#23+28 --> 23%2B28
#rule: replace + with %2B
#23/28 --> 23%2F28
#rule: replace / with %2F
#3 / 4 --> 3%20%2F%204
#replace all spaces with %20 
#replace ? with %3F

#altererations are not needed for: * , - , **  

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
        except: 
            continue #skip over the pods without titles
        else:
            if pod.attrib['title']=='Result' or pod.attrib['title']=='Exact result':
                solution = pod[0][0].text 
    return solution

def main():
    myinput = "1/58"
    print getWAsolution(myinput)

main()



