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


DATABASE_DICT, ANALYSED_DICT, HUMAN_DICT = {}, {}, {}

# Relevant paths
LOG_PATH = 'small.log'
DATABASE_DICT_PATH = 'log_dict.json'
ANALYSED_LOG_PATH = 'log_anal.json'
HUMAN_LOG = 'log_final.json'

# Timestamp format before log message
timestampFormat = '(\d{2})/(\d{2})/(\d{2})\s(\d{2}):(\d{2}):(\d{2})'
logAdditions = '(\s\s0\s*)'

def dictDatabaseBuild(DATABASE_DICT):
    # Open log file in read only mode
    _file = open(LOG_PATH, 'r')

    if os.stat(DATABASE_DICT_PATH).st_size != 0:
        with open(DATABASE_DICT_PATH) as f:
            DATABASE_DICT = json.load(f)
        os.replace(DATABASE_DICT_PATH, 'Old_' + DATABASE_DICT_PATH)

    for line in _file:
        cleanLine = re.sub(timestampFormat, '', line).replace('\n','')
        cleanLine = re.sub(logAdditions, '', cleanLine)

        # Hash the message, this will be used as key value in the dictionary
        entryHash = str(int(hashlib.sha512(cleanLine.encode('utf-8')).hexdigest(), 16))
        # Search for hashed message in the dictionary
        if entryHash not in DATABASE_DICT:
            DATABASE_DICT[entryHash] = (cleanLine, 'new')
        
    _file.close()

    with open(DATABASE_DICT_PATH, 'w') as f:
        json.dump(DATABASE_DICT, f)


def dictAnalysedBuild(ANALYSED_DICT):
    # Open log file in read only mode
    _file = open(LOG_PATH, 'r')
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
        if entryHash in ANALYSED_DICT:
            # If message is found get it temporarily
            entryFound = ANALYSED_DICT[entryHash]
            # Increment the message counter 
            countIncrement = entryFound[1] + 1
            # Create new tuple with the updated counter
            updatedEntry = (entryFound[0], countIncrement)
            # Overwrite value with updated tuple
            ANALYSED_DICT[entryHash] = updatedEntry
        else:
            # Add new tuple to the dictionary if not present
            ANALYSED_DICT[entryHash] = (cleanLine, 1)
        
    _file.close()
    with open(ANALYSED_LOG_PATH, 'w') as f:
        json.dump(ANALYSED_DICT, f)

def dictHumanBuild(DATABASE_DICT, HUMAN_DICT):
     # Open log file in read only mode
    _file = open(LOG_PATH, 'r')

    if os.stat(DATABASE_DICT_PATH).st_size != 0:
        with open(DATABASE_DICT_PATH) as f:
            DATABASE_DICT = json.load(f)
    counter = 0    
    for line in _file:
        cleanLine = re.sub(timestampFormat, '', line).replace('\n','')
        cleanLine = re.sub(logAdditions, '', cleanLine)

        # Hash the message, this will be used as key value in the dictionary
        entryHash = str(int(hashlib.sha512(cleanLine.encode('utf-8')).hexdigest(), 16))
        # Search for hashed message in the dictionary
        if entryHash in DATABASE_DICT:
            # FIX THIS!!!
            if DATABASE_DICT[entryHash][1] is 'new':
                HUMAN_DICT[str(counter)] = DATABASE_DICT[entryHash][1]
                counter += 1

        
    _file.close()

    with open(HUMAN_LOG, 'w') as f:
        json.dump(HUMAN_DICT, f)


dictDatabaseBuild(DATABASE_DICT)
dictAnalysedBuild(ANALYSED_DICT)
dictHumanBuild(DATABASE_DICT, HUMAN_DICT)

    # with open(DATABASE_DICT_PATH) as f:
    #     my_dict = json.load(f)
