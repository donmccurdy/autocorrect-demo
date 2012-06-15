#!/usr/bin/env python
import xmlrpclib
import sys

#Proxy for spellchecker.py
#This script runs each time a word is submitted to be spellchecked.
#It connects to the XML-RPC server, which is running constantly,
#to prevent the XML-RPC server from needing to restart and reload
#its data every time a query comes in.

try:
	myProxy = xmlrpclib.ServerProxy('http://206.217.131.124:9000')
	result = myProxy.spellcheck(sys.argv[1])
	print result[1]
except Exception:
	print "SERVER_ERROR" 
