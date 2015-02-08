__author__ = 'calvindudek'

from util import JsonHandler as json
import document

class Evaluation():

  def __init__(self, classifier):
    self.ec_list = list()      # every element is a tuple (sentence, ec)
    self.classifier = classifier
    self.labels = self.classifier.trigger_fh.labels
    self.arg_labels = self.classifier.argument_fh.labels


  def readResultsFromFile(self, docs):
    # docs = json.getJsonDocuments(path)
    for doc in docs:
      doc_obj = document.Document(doc)
      for sentence in doc_obj.getSentences():
        for ec in sentence.getEventCandidates():
          self.ec_list.append([sentence, ec])



  def getLabelMetrics(self):
    named_matrix = dict()
    cm_results = dict()


    for label in self.labels:
      named_matrix[label] = dict()

      for label_inner in self.labels:
        named_matrix[label][label_inner] = 0.0

    for ec_element in self.ec_list:
      actual_class = ec_element[1].gold
      predicted_class = self.classifier.classifyTrigger(ec_element[0], ec_element[1])
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


  def getResults(self, arg_type):


    label_metrics = self.getLabelMetrics()

    # print label_metrics
    # NxN Matrix for Error Analysis
    print "##############################"
    print "### %s LABEL CONFUSION MATRIX ###" % arg_type.upper()
    print "###############################"
    print label_metrics

    precision_sum = 0
    recall_sum = 0
    n = 0
    print "##############################"
    print "### %s MICRO RESULTS ###" % arg_type.upper()
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
    print "### %s MACRO RESULTS ###" % arg_type.upper()
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