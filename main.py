#!/usr/bin/env python
#Author ilkkayli

import urllib2
import datetime

rawSrc="rawSrc.txt" # kasittelytiedosto

# opens Jenkins page where Robot Framework jobs are and retrieves source of the page. Replace url-string "http://" with yours.
def retrieveSource():
    
    try:
        wRawSrc=open(rawSrc,"w")
        locPage = "http://"
        url = urllib2.urlopen(locPage)
        source = url.read()
        url.close()
        wRawSrc.write(source)
        wRawSrc.close()
        parseRobotResults()
        
    except urllib2.URLError:
        if "http://" in locPage:
            print "Exception: please replace the default url with the url on your Jenkins page."
        else:
            print "Exception: could not open the specified URL."
    
def parseRobotResults():
    
    totalPassedTests = 0
    totalTests = 0
    passRate = 0.00
    
    # iterates thru the source file and calculates the pass rate
    rRawSrc = open(rawSrc, "r")
    for line in rRawSrc:
        if "passed" in line:
            line = line.split("<img src=")
            line = line[0].replace(" passed", "")
            line = line.split("/")
            totalPassedTests = totalPassedTests + int(line[0])
            totalTests = totalTests + int(line[1])
    rRawSrc.close()
    passRate = float(totalPassedTests) / float(totalTests) * 100
    passRate = str(passRate)
    
    #write result on to the log file.  A one line per day.    
    today =  str(datetime.date.today())        
    resultLine = today + "  :  " + passRate[:4] + "%" + "\n"
    
    with open("Robot_results.txt","a+") as robotResultsLog:
        robotResultsLog.write(resultLine)            
   
retrieveSource()