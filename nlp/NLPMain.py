__author__ = 'calvindudek'

from TextFeatures import NLP
from os import listdir
from os.path import isfile, join
import json
import nltk

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
  # start = time.gmtime()
  users = getFiles("../data/")


  for user in users:
    nlp = NLP(user)

    pos_words_features = nlp.getPosTweetDist()
    pos_description_features = nlp.getPosDescriptionDist()

    print pos_words_features
    print pos_description_features



if __name__ == '__main__':
  main()