from os import listdir
from os.path import isfile, join
import json
from pprint import pprint
import csv

import Sample
path = "data"




def encode_type(type):
    type = type.lower()
    encoded = []
    #features.append(twitName)
    if(type[0]=='i'):
        encoded.append(1)
    else:
        encoded.append(0)
    if(type[1]=='s'):
        encoded.append(1)
    else:
        encoded.append(0)
    if(type[2]=='f'):
        encoded.append(1)
    else:
        encoded.append(0)
    if(type[3]=='p'):
        encoded.append(1)
    else:
        encoded.append(0)
    return encoded

def main():
    files = [ f for f in listdir(path) if isfile(join(path,f)) ]
    with open('samples.csv', 'w') as outfile:
        for file in files:
            sample = Sample.Sample("data/{}".format(file))
            print "{}: {}".format(sample.type, sample.twitName)
            if not sample.data:
                continue
            features = []
            #features.append(twitName)
            features.extend(encode_type(sample.type))
            features.extend(sample.data)
            outwriter = csv.writer(outfile, lineterminator= '\n')
            outwriter.writerow(features)

if __name__ == '__main__':
  main()