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
  # start = time.gmtime()
  users = getFiles("../data/")
  tags = {}
  for user in users:
    nlp = NLP(user)

    for key, val in nlp.profile_word_count_by_pos.items():
      try:
        print "%s: %.4f" % (key, val/nlp.profile_word_count)
      except:
        print "%s: %.4f" % (key, 0.0)

    for key, val in nlp.tweet_word_count_by_pos.items():
      print "%s: %.4f" % (key, val/nlp.tweet_word_count)

  print tags


if __name__ == '__main__':
  main()


