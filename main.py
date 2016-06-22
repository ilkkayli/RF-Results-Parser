#Author ilkkayli

import urllib2
import datetime
import formJSON
import json
import requests

api_url =  "http://localhost:8888/" # URL to your REST API
jenkins_url = "http://" # URL where your Robot Framework jobs are located on your Jenkins web page
rawSrc = "rawSrc.txt" # Mandatory file for data manipulation, don't change or remove.

# opens Jenkins page where Robot Framework jobs are and retrieves source of the page. Replace url-string "http://" with yours.
def retrieveSource():
    
    try:
        wRawSrc=open(rawSrc,"w")
        url = urllib2.urlopen(jenkins_url)
        source = url.read()
        url.close()
        wRawSrc.write(source)
        wRawSrc.close()
        parseRobotResults()

    except urllib2.URLError:
        if "http://" in jenkins_url:
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
    
    '''if today not in open('Robot_results.txt').read():
       with open('Robot_results.txt','a+') as robotResultsLog:
        robotResultsLog.write(resultLine)'''
    
    setJSONdata = "[" + '"' + today + '",' + passRate[:4] + "]"
    passRate = passRate[:4]

    # Checks if there already is a value in db for current date. If not, POST a new date:value pair. If yes, PUT existing values. 
    values = ApiGET()
    value_updated = 1
    for key in values:
        new_value = str(key)
        new_value = new_value.split(',')
        new_value = new_value[0].split(':')
        if str(today) in new_value[1]:
            value_updated = 0
            ApiPUT(today, passRate)
    if value_updated == 1:
        ApiPOST(today, passRate)        
    
    # Create JSON dataset for ZingChart. This has to be written into a *.json file.               
    for key in values:
        new_value = str(key)
        new_value = new_value.split(',')
        new_date = new_value[0].split(':')
        zingchart_line = new_value[0] + ':' + new_value[1]
        zingchart_line = zingchart_line.split(':')
        zingchart_line = zingchart_line[1] + ',' + zingchart_line[3].replace("'","")
        zingchart_line = zingchart_line.replace("'", '"')
        zingchart_line = zingchart_line.replace('u', '')
        zingchart_line = zingchart_line.replace(' "2', '["2')
        zingchart_line = zingchart_line + "]"
        formJSON.formJSON(zingchart_line)

# Function adds a new document on to the db collection  
def ApiPOST(date, passRate):
   
    data = {"date": str(date), "passRate": str(passRate)}
    resp = requests.post(api_url, json=data)
    if resp.status_code != 201:
        raise ApiError('POST {}'.format(resp.status_code))
    print('Added new values.')

# Function gets values from the db    
def ApiGET():
    
    resp = requests.get(api_url)
    if resp.status_code != 200:
        raise ApiError('GET {}'.format(resp.status_code))
    result = resp.json()
    return result    

# Function updates a document on the db collection
def ApiPUT(today, passRate):   

    data = {"date": str(today), "passRate": str(passRate)}
    resp = requests.put(api_url, json=data)
    if resp.status_code != 202:
        raise ApiError('PUT {}'.format(resp.status_code))
    print('Value updated.') 
   
retrieveSource()