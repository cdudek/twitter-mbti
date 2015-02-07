__author__ = 'gee'

from FeatureTemplateHandler import FTHandler
import csv

class FeatureHandler():
  def __init__(self):
    self.features = dict()
    self.feature_dict = dict()
    self.labels = list()
    self.weight_vector = list()
    self.feature_vectors = dict(list())   # one vector for each label
    self.feature_dict_length = 0
    self.ft_handler = FTHandler()

  def addFeature(self, label, word, value):
    if label not in self.features:
      self.features[label] = {word: value}
    else:
      if word in self.features[label]:
        self.features[label][word] += value
      else:
        self.features[label][word] = value

  def addFeatureToDict(self, feature):

      if feature not in self.feature_dict:
        self.feature_dict[feature] = len(self.feature_dict)
      # print self.indexed_feature_vector[word]

  def getFeatures(self):
    return self.features


  def getWordsByLabel(self, label):
    return {k: v for (k, v) in self.features.iteritems() if label in k}.values()

  # can be used to check whether feature is active
  # e.g.if stem of word returns non empty list, feature is active
  def getLabelsByWord(self, word):
    words = []
    for f, v in self.features.iteritems():
      if word in v:
        words.append(f)
    return words

  def writeFeaturesToFile(self):
    with open('features.csv', 'wb') as file:
      for f in self.feature_dict.values():
        file.write("%d\n" % f)

  #     for f in self.weight_vector:
  def writeWeightVectorToFile(self):
    with open('weight_vector.csv', 'wb') as file:
      lenght = len(self.weight_vector)
      for f in self.weight_vector:
        file.write("%d" % f)
        if lenght > 0:
          file.write(", ")
        lenght -= 1