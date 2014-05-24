# -*- coding: utf-8 -*-
"""
Created on Tue May 06 23:51:02 2014

@author: Ethan
"""

import urllib2
import re
import os


for names in os.listdir('..\BoxScoreLinks'):
    with open(os.path.join('..\BoxScoreLinks',names),'r') as f1: #Read in each year's game URLs
        with open('Player'+names,'w') as f2: #Setup output file to write
            totalPlayerLinks = [] #Player URL list for each year
            for lines in f1:
                url=lines.split('"')[1] #Extract URL
                
                try:
                    ufile=urllib2.urlopen(url) #Connect to URL
                except urllib2.HTTPError, error:
                    print error.read() #If there's an error, print it and try again
                    try:
                        ufile=urllib2.urlopen(url)
                    except urllib2.HTTPError, error:
                        print error.read() + '\n'
                        print 'Could not connect to \n' + str(url) + '\n'
                    
                #Find all player links
                singlePagePlayerLinks=re.findall(r'"http://espn.go.com/mlb/player/_/id/[\w\.\-\/\_]+"',ufile.read())
                #Add links from page to total list         
                totalPlayerLinks.extend(singlePagePlayerLinks)    
            totalPlayerLinks=sorted(totalPlayerLinks) #Sort the list because why not?
            totalPlayerLinksSet=set(totalPlayerLinks) #Remove duplicates
            for links in totalPlayerLinksSet: #Write all player links for that year
                f2.write(links+'\n')                
        f2.close()
    f1.close()
                

