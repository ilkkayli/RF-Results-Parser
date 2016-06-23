# RF-Results-Parser

## What is does?
------------

Used for gathering Robot Framework test results from Jenkins jobs and calculating overall pass rate.
Retrieves test status information of RF tests from Jenkins and stores them in a database. There is a 
REST-interface with GET/POST/PUT/DELETE methods supported.
Updates a *.json-file that contains test status information from last 10 days. This file is read by zingchart.js
which creates nice HTML graphs. 

## Prerequisities/depedencies
--------------------------

* [Python 2.x] (https://www.python.org/)
* [MongoDB] (https://www.mongodb.com/)
* [Falcon] (https://falconframework.org/) (requires: six, mimeparse)
	
	`pip install falcon`
		
* [Waitress] (http://docs.pylonsproject.org/projects/waitress/en/latest/)

* PyMongo

	`pip install pymongo`
	
* Column named "Robot Results" added for every job on the Jenkins web page.

## Installation/configuration
--------------------------

1) Create a database called 'Test' with collection "firstcollection" on your MongoDB instance and make it run on localhost:27017 (the default port).
	Note: that you can set db and collection names whatever you like, but they must be configured also on "app.py" on line 7.
2) Create a working directory. You can use the C:\data\ -folder created by the MongoDB installation.
3) Drop files "wsgisrv.py", "app.py", "resources.py", "formJSON.py", "main.py" and "data.json" to the working directory.
4) Set the jenkins_url -variable on the "main.py"to the url where your Jenkins jobs are.

## Running
-------

Start the WSGI-server in the command prompt: 

	C:\python "C:\<path_to_working directory>\wsgisrv.py

## Protips
-------
