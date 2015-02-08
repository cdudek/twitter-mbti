__author__ = 'calvindudek'

from nlp.TextFeatures import NLP
import time
from os import listdir
from os.path import isfile, join
import json

def getFiles(path):
  # print self.path
  results = list()
  files = [f for f in listdir(path) if isfile(join(path, f))]
  for file in files:
    if(file.endswith(".json")):
      json_file = json.loads(open(path + file).read())
      results.append(json_file)
  return results

def main():
  print time.localtime()
  start = time.gmtime()
  users = getFiles("../data/")
  tags = {}
  for user in users:
    nlp = NLP(user)
    nlp.countWords()
    print time.gmtime() - start
    start = time.gmtime()
  print tags


if __name__ == '__main__':
  main()


