#figure out how to use wolfa-alpha's API

import sys
import argparse
import urllib #this allows me to read remote website as though it were a file
import urllib2 #this is a newer version of urllib
import httplib
from xml.dom.minidom import parseString #what I get thru W-A's API is an XML file
import xml.etree.ElementTree as ET #this may be a better alternative to minidom
import wolframalpha


t = urllib.urlopen(url)
t.read()

