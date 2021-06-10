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
# File names
LOG_N = 'small.log'
DATABASE_DICT_N = 'log_dict.json'
ANALYSED_LOG_N = 'analysed.json'
HUMAN_LOG_N = 'human.json'
# Relevant paths
LOG_FOLDER = 'logs/'
LOG_PATH = LOG_FOLDER + LOG_N
DATABASE_DICT_PATH = LOG_FOLDER + DATABASE_DICT_N
ANALYSED_LOG_PATH = LOG_FOLDER + ANALYSED_LOG_N
HUMAN_LOG = LOG_FOLDER + HUMAN_LOG_N

# Timestamp format of base log
TIMESTAMP_LOG_OG = '(\d{2})/(\d{2})/(\d{2})\s(\d{2}):(\d{2}):(\d{2})'
LOG_CLUTTER = '(\s\s0\s*)'


class LogAnalyser():
    def build_database_dict(self, log_path: str):
        # Open log file in read only mode
        _file = open(log_path, 'r')

        # Check if dictionary exists and create it if necessary
        if not os.path.isfile(DATABASE_DICT_PATH):
            _temp = open(DATABASE_DICT_PATH, 'w+')
            _temp.write('{}')
            _temp.close()

        with open(DATABASE_DICT_PATH) as f:
            DATABASE_DICT = json.load(f)
        os.replace(DATABASE_DICT_PATH, LOG_FOLDER + 'old_' + DATABASE_DICT_N)

        for line in _file:
            cleanLine = re.sub(TIMESTAMP_LOG_OG, '', line).replace('\n', '')
            cleanLine = re.sub(LOG_CLUTTER, '', cleanLine)
            # Hash the message, this will be used as key value in the dictionary
            entryHash = str(
                int(hashlib.sha512(cleanLine.encode('utf-8')).hexdigest(), 16))
            # Search for hashed message in the dictionary
            if entryHash not in DATABASE_DICT:
                DATABASE_DICT[entryHash] = (cleanLine, 'new', 'WARN')

        _file.close()

        with open(DATABASE_DICT_PATH, 'w') as f:
            json.dump(DATABASE_DICT, f)

    def analyse_log(self, log_path: str):
        # Open log file in read only mode
        try:
            _file = open(log_path, 'r')

            # Check if dictionary exists and create it if necessary
            if not os.path.isfile(DATABASE_DICT_PATH):
                _temp = open(DATABASE_DICT_PATH, 'w+')
                _temp.write('{}')
                _temp.close()
            # Declare total log line counter
            line_count = 0

            for line in _file:
                # Count lines in the log
                if line != '\n':
                    line_count += 1

                # timeStamp = re.search(TIMESTAMP_LOG_OG, line)
                # if timeStamp:
                #     print(timeStamp.group())

                cleanLine = re.sub(TIMESTAMP_LOG_OG, '',
                                   line).replace('\n', '')
                cleanLine = re.sub(LOG_CLUTTER, '', cleanLine)
                # Hash the message, this will be used as key value in the dictionary
                entryHash = str(
                    int(hashlib.sha512(cleanLine.encode('utf-8')).hexdigest(), 16))
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

        except Exception as Argument:
            print('An exception was encountered: {}'.format(str(Argument)))

    def build_human_log(self, log_path: str):
        # Open log file in read only mode
        _file = open(log_path, 'r')

        # Load dictionary
        if os.stat(DATABASE_DICT_PATH).st_size != 0:
            with open(DATABASE_DICT_PATH) as f:
                DATABASE_DICT = json.load(f)

        counter = 0
        for line in _file:
            cleanLine = re.sub(TIMESTAMP_LOG_OG, '', line).replace('\n', '')
            cleanLine = re.sub(LOG_CLUTTER, '', cleanLine)

            # Hash the message, this will be used as key value in the dictionary
            entryHash = str(
                int(hashlib.sha512(cleanLine.encode('utf-8')).hexdigest(), 16))
            # Search for hashed message in the dictionary
            if entryHash in DATABASE_DICT:
                # FIX THIS!!!
                if DATABASE_DICT[entryHash][1] == 'new':
                    HUMAN_DICT[str(counter)] = DATABASE_DICT[entryHash][1]
                    counter += 1

        _file.close()

        with open(HUMAN_LOG, 'w') as f:
            json.dump(HUMAN_DICT, f)


LogAnalyser().build_database_dict(LOG_PATH)
LogAnalyser().analyse_log(LOG_PATH)
LogAnalyser().build_human_log(LOG_PATH)

# with open(DATABASE_DICT_PATH) as f:
#     my_dict = json.load(f)
