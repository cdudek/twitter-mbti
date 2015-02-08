__author__ = 'calvindudek'

import json

class Evaluation():

  def __init__(self):
    self.predictions = list()      # every element is a tuple (sentence, ec)
    self.path = "../accuracy_results.json"
    self.labels = ['INFP','INFJ','INTJ','INTP','ISFJ','ISFP','ISTJ','ISTP','ENFJ','ENFP','ENTJ','ENTP','ESFJ','ESFP','ESTJ','ESTP']



  def readResultsFromFile(self):
    self.predictions = json.loads(open(self.path).read())
    print self.predictions
    # doc_obj = document.Document(doc)




  def getLabelMetrics(self):
    named_matrix = dict()
    cm_results = dict()


    for label in self.labels:
      named_matrix[label] = dict()

      for label_inner in self.labels:
        named_matrix[label][label_inner] = 0.0

    for element in self.predictions:
      actual_class = element["type"]
      predicted_class = element["prediction"]
      named_matrix[actual_class][predicted_class] += 1.0

    for label in self.labels:
      cm_results[label] = self.getTwoByTwoConfusionMatrix(named_matrix, self.labels, label)

    print named_matrix
    return cm_results



  def getTwoByTwoConfusionMatrix(self, named_matrix, labels, label):
    cm = {"truePositive": 0.0, "falseNegative": 0.0, "falsePositive": 0.0, "trueNegative": 0.0}
    # print named_matrix
    cm["truePositive"] = named_matrix[label][label]
    # print named_matrix[label]
    cm["falseNegative"] = sum(named_matrix[label].values()) - cm["truePositive"]

    for label_inner in labels:
      if label != label_inner:
        cm["falsePositive"] = cm.get("falsePositive", 0.0) + named_matrix[label_inner][label]
        cm["trueNegative"] = cm.get("trueNegative", 0.0) + named_matrix[label_inner][label_inner]
    return cm


  def getResults(self):


    label_metrics = self.getLabelMetrics()

    # print label_metrics
    # NxN Matrix for Error Analysis
    print "##############################"
    print "### LABEL CONFUSION MATRIX ###"
    print "###############################"
    print label_metrics

    precision_sum = 0
    recall_sum = 0
    n = 0
    print "##############################"
    print "### MICRO RESULTS ###"
    print "###############################"
    for label in label_metrics:
      if label != "None":
        cm = label_metrics[label]
        try:
          print "{}: Precision: {:.2%}".format(label, self.precision(cm))
          print "{}: Recall: {:.2%}".format(label, self.recall(cm))
          print "{}: F1 Measure: {:.2%}".format(label, self.f1measure(cm))

          precision_sum += self.precision(cm)
          recall_sum += self.recall(cm)
          n += 1
        except:
          pass

    precision = precision_sum / n
    recall = recall_sum / n
    f1 = self.total_f1measure(precision, recall)
    print "\n"
    print "#############################"
    print "### MACRO RESULTS ###"
    print "#############################"


    print "Precision: {:.2%}".format(precision)
    print "Recall: {:.2%}".format(recall)
    print "F1 Measure: {:.2%}\n".format(f1)



  def total_f1measure(self, precision, recall):
    return (2*precision*recall)/(precision+recall)

  def precision(self, cm):
    return cm["truePositive"] / (cm["truePositive"] + cm["falsePositive"])

  def recall(self, cm):
    return cm["truePositive"] / (cm["truePositive"] + cm["falseNegative"])

  def f1measure(self, cm):
    precision = self.precision(cm)
    recall = self.recall(cm)
    return (2*precision*recall)/(precision+recall)