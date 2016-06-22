#!/usr/bin/env python
# Function updates a json file which contains datestamps and pass rates.
# It takes the newest data as an argument and removes the oldest from the list. Totally fourteen data lines are maintained.

from collections import deque
import os

newDataFile = "new_data.json"

def formJSON(value):

    newValue =  "               " + value # This modification is needed for keeping data structure consistent.
    queue = []    
    
    # Read data from json-file and form a queue for data handling
    with open('data.json') as fp:
        for i, line in enumerate(fp):
            if i > 23 and i < 38:
               queue.append(line)
        
        queue = deque(queue)
        queue.popleft()
        queue.append(newValue)

    # Write data lines into a new file.
    with open('data.json', 'r+') as file_in:        
        wNewDataFile=open(newDataFile,"w")    
        for i, line in enumerate(file_in):
            if i > 23 and i < 36:
               newLine = queue.popleft()
               line = line.replace(line, newLine)
            elif i == 36:
               newLine = queue.popleft()
               newLine = newLine.split(']')
               newLine = newLine[0] + '],' + newLine[1]
               line = line.replace(line, newLine)
            elif i == 37:
               newLine = queue.popleft()
               line = line.replace(line, newLine)
               line = line + "\n"
            
            wNewDataFile.write(line)
        wNewDataFile.close()
    
    os.remove("data.json")
    os.rename("new_data.json", "data.json")
