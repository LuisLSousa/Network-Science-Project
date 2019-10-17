from os.path import join
import json

def printResultsToJson(logs, dir):
    with open(join(dir, 'logs.json'), 'w') as outfile:
        json.dump(logs, outfile)
