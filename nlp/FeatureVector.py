__author__ = 'gee'

class FeatureVector():
  def __init__(self, name):
    self.featurename = name
    self.features = dict()
    self.valuekeys = list()

  def addFeature(self, label, value, count):
    label = "%s-%s" % (self.featurename, label)
    if label not in self.features:
      self.features[label] = {value: count}
    else:
      if value in self.features[label]:
        self.features[label][value] += count
      else:
        self.features[label][value] = count

    if value not in self.valuekeys:
      self.valuekeys.append(value)

  def getFeatures(self):
    return self.features

  def length(self):
    length = 0
    for ft in self.features:
      length += len(self.features[ft])
    return length

  def getFeatureVector(self):
    feature_vector = dict()
    for ft in self.features:
      for f in self.features[ft].keys():
        feature_vector[f] = 0.0
    # print list(feature_vector.values())
    return feature_vector


  def getValuesByFeature(self, feature):
    feature =  "%s-%s" % (self.featurename, feature)
    return {k: v for (k, v) in self.features.iteritems() if feature in k}.values()

  # can be used to check whether feature is active
  # e.g.if stem of word returns non empty list, feature is active
  def getFeaturesByValue(self, value):
    features = []
    for f, v in self.features.iteritems():
      if value in v:
        features.append(f)
    return features
