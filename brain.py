import re
import hashlib
import json
import os

# Main program : brain.py
# Dictionary database: log_dict.json
#   
# Dictionary contains:
#   Key = Hashed log message ( after it was stripped of unnecessary additions )
#   Value = Tuple:
#       0: log message
#       1: meaning of the message
#

# Main variables
DatabaseDict = {}
AnalysedDict = {}
HumanDict = {}
logFile = 'small.log'
logDictDatabase = 'log_dict.json'
logDictAnalysed = 'log_anal.json'
logHuman = 'log_final.json'

# Timestamp format before log message
timestampFormat = '(\d{2})/(\d{2})/(\d{2})\s(\d{2}):(\d{2}):(\d{2})'
logAdditions = '(\s\s0\s*)'

def dictDatabaseBuild(DatabaseDict):
    # Open log file in read only mode
    _file = open(logFile, 'r')

    if os.stat(logDictDatabase).st_size != 0:
        with open(logDictDatabase) as f:
            DatabaseDict = json.load(f)
        os.replace(logDictDatabase, 'Old_' + logDictDatabase)

    for line in _file:
        cleanLine = re.sub(timestampFormat, '', line).replace('\n','')
        cleanLine = re.sub(logAdditions, '', cleanLine)

        # Hash the message, this will be used as key value in the dictionary
        entryHash = str(int(hashlib.sha512(cleanLine.encode('utf-8')).hexdigest(), 16))
        # Search for hashed message in the dictionary
        if entryHash not in DatabaseDict:
            DatabaseDict[entryHash] = (cleanLine, 'new')
        
    _file.close()

    with open(logDictDatabase, 'w') as f:
        json.dump(DatabaseDict, f)


def dictAnalysedBuild(AnalysedDict):
    # Open log file in read only mode
    _file = open(logFile, 'r')
    # Declare total log line counter
    line_count = 0

    for line in _file:
        # Count lines in the log
        if line != '\n':
            line_count += 1
        
        # timeStamp = re.search(timestampFormat, line)
        # if timeStamp:
        #     print(timeStamp.group())

        cleanLine = re.sub(timestampFormat, '', line).replace('\n','')
        cleanLine = re.sub(logAdditions, '', cleanLine)
        # Hash the message, this will be used as key value in the dictionary
        entryHash = str(int(hashlib.sha512(cleanLine.encode('utf-8')).hexdigest(), 16))
        # Search for hashed message in the dictionary
        if entryHash in AnalysedDict:
            # If message is found get it temporarily
            entryFound = AnalysedDict[entryHash]
            # Increment the message counter 
            countIncrement = entryFound[1] + 1
            # Create new tuple with the updated counter
            updatedEntry = (entryFound[0], countIncrement)
            # Overwrite value with updated tuple
            AnalysedDict[entryHash] = updatedEntry
        else:
            # Add new tuple to the dictionary if not present
            AnalysedDict[entryHash] = (cleanLine, 1)
        
    _file.close()
    with open(logDictAnalysed, 'w') as f:
        json.dump(AnalysedDict, f)

def dictHumanBuild(DatabaseDict, HumanDict):
     # Open log file in read only mode
    _file = open(logFile, 'r')

    if os.stat(logDictDatabase).st_size != 0:
        with open(logDictDatabase) as f:
            DatabaseDict = json.load(f)
    counter = 0    
    for line in _file:
        cleanLine = re.sub(timestampFormat, '', line).replace('\n','')
        cleanLine = re.sub(logAdditions, '', cleanLine)

        # Hash the message, this will be used as key value in the dictionary
        entryHash = str(int(hashlib.sha512(cleanLine.encode('utf-8')).hexdigest(), 16))
        # Search for hashed message in the dictionary
        if entryHash in DatabaseDict:
            # FIX THIS!!!
            if DatabaseDict[entryHash][1] is 'new':
                HumanDict[str(counter)] = DatabaseDict[entryHash][1]
                counter += 1

        
    _file.close()

    with open(logHuman, 'w') as f:
        json.dump(HumanDict, f)


dictDatabaseBuild(DatabaseDict)
dictAnalysedBuild(AnalysedDict)
dictHumanBuild(DatabaseDict, HumanDict)

    # with open(logDictDatabase) as f:
    #     my_dict = json.load(f)
