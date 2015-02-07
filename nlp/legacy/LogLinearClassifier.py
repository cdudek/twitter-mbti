__author__ = 'calvindudek'


# import document
from FeatureHandler import FeatureHandler
import operator
import time
from scipy.sparse import csr_matrix
from scipy import *
import numpy

class LinearClassifier:
  def __init__(self):
    self.trigger_fh = FeatureHandler()         # stores triggers and weight vector
    self.argument_fh = FeatureHandler()         # stores arguments and weight vector
    self.count_docs = 0
    self.none_counter = 0
    self.my_counter = 0
    self.NONE_DOWNSAMPLE = 11


  def trainTriggerLabels(self, docs):
    # docs = json.getJsonDocuments(trainingpath)
    for doc in docs:
      doc_obj = document.Document(doc)
      for sentence in doc_obj.getSentences():
        for ec in sentence.getEventCandidates():
          if ec.gold not in self.trigger_fh.labels:
            self.trigger_fh.labels.append(ec.gold)


  def trainArgumentLabels(self, docs):
    # docs = json.getJsonDocuments(trainingpath)
    for doc in docs:
      doc_obj = document.Document(doc)
      for sentence in doc_obj.getSentences():
        for ec in sentence.getEventCandidates():
          for arg in ec.getArguments():
            if arg.gold not in self.argument_fh.labels:
              self.argument_fh.labels.append(arg.gold)


  def trainTriggers(self, docs):
    #docs = json.getJsonDocuments(trainingpath)
    self.trainTriggerLabels(docs)

    for doc in docs:
      self.count_docs +=1
      doc_obj = document.Document(doc)
      # create trigger_fh
      for sentence in doc_obj.getSentences():
        self.extractTriggerFeatures(sentence)
    self.trigger_fh.weight_vector = csr_matrix([0] * self.trigger_fh.feature_dict_length)
    print "Train Trigger done"


  def trainArguments(self, docs):
    #docs = json.getJsonDocuments(trainingpath)
    self.trainArgumentLabels(docs)

    for doc in docs:
      self.count_docs +=1
      doc_obj = document.Document(doc)
      # create trigger_fh
      for sentence in doc_obj.getSentences():
        self.extractArgumentFeatures(sentence)
    self.argument_fh.weight_vector = csr_matrix([0] * len(self.argument_fh.feature_dict))
    print self.argument_fh.labels
    print "Train Arguments done"


  def extractTriggerFeatures(self, sentence):
    for ec in sentence.getEventCandidates():
      if ec.gold == 'None':
        self.none_counter += 1
      if ec.gold != 'None' or self.none_counter % self.NONE_DOWNSAMPLE == 0:
        for label in self.trigger_fh.labels:
          features = self.trigger_fh.ft_handler.createTriggerFeaturesWithTemplates(sentence, ec, label)
          for feature in features:
            self.trigger_fh.addFeatureToDict(feature)
    self.trigger_fh.feature_dict_length = len(self.trigger_fh.feature_dict)

  def extractArgumentFeatures(self, sentence):
    arg_none_counter = 0
    # self.weight_vectors["None"] = list()
    for ec in sentence.getEventCandidates():
      if ec.gold == 'None':
        self.none_counter += 1

      if ec.gold != 'None' or self.none_counter % self.NONE_DOWNSAMPLE == 0:
        for argument in ec.getArguments():

          if argument.gold == "None":
            arg_none_counter += 1
          if argument.gold != "None" or arg_none_counter % self.NONE_DOWNSAMPLE == 0:
            for label in self.argument_fh.labels:
              features = self.argument_fh.ft_handler.createArgumentFeaturesWithTemplates(sentence, argument, ec, label)
              for feature in features:
                self.argument_fh.addFeatureToDict(feature)
    self.argument_fh.feature_dict_length = len(self.argument_fh.feature_dict)


  def phiTrigger(self, sentence, ec, label):
    activations = list()
    features = self.trigger_fh.ft_handler.createTriggerFeaturesWithTemplates(sentence, ec, label)

    # get activations for current event candidate
    for feature in features:
      try:
        value = self.trigger_fh.feature_dict[feature]
        activations.append(value)
      except:
        pass

    # Create sparse Matrix for activations
    act_length = len(activations)
    data = array([1] * act_length)
    row = array([0] * act_length)
    col = array(activations)
    sparse_matrix = csr_matrix((data, (row, col)), shape=(1, self.trigger_fh.feature_dict_length))

    return sparse_matrix     # returns sparse matrix

  def phiArgument(self, sentence, arg, ec, label):
    activations = list()
    features = self.argument_fh.ft_handler.createArgumentFeaturesWithTemplates(sentence, arg, ec, label)

    # get activations for current event candidate
    for feature in features:
      try:
        value = self.argument_fh.feature_dict[feature]
        activations.append(value)
      except:
        pass

    # Create sparse Matrix for activations
    act_length = len(activations)
    data = array([1] * act_length)
    row = array([0] * act_length)
    col = array(activations)
    sparse_matrix = csr_matrix((data, (row, col)), shape=(1, self.argument_fh.feature_dict_length))
    # print "returned sparse matrix"
    return sparse_matrix     # returns sparse matrix


  def classifyTrigger(self, sentence, ec):
    dot_products = dict()
    # calculate dot product for every label
    for label in self.trigger_fh.labels:
      self.trigger_fh.feature_vectors[label] = self.phiTrigger(sentence, ec, label)
      dot_products[label] = self.trigger_fh.feature_vectors[label].dot(self.trigger_fh.weight_vector.toarray()[0])

    # take label with highest score
    argmax = max(dot_products.iteritems(), key=operator.itemgetter(1))
    return argmax[0]

  def classifyArgument(self, sentence, arg, ec, labels=[]):
    dot_products = dict()
    if labels == []:
      labels = self.argument_fh.labels
    # calculate dot product for every label

    for label in labels:
      self.argument_fh.feature_vectors[label] = self.phiArgument(sentence, arg, ec, label)
      dot_products[label] = self.argument_fh.feature_vectors[label].dot(self.argument_fh.weight_vector.toarray()[0])

    # take label with highest score
    argmax = max(dot_products.iteritems(), key=operator.itemgetter(1))
    return argmax

  def classifyJointly(self, sentence, ec):
    dot_products = dict()
    args_guesses_by_label = dict()
    for label in self.trigger_fh.labels:
      # CASE 1 NONE
      if label == "None":
        arg_score = 0
        self.trigger_fh.feature_vectors[label] = self.phiTrigger(sentence, ec, label)
        dot_products[label] = self.trigger_fh.feature_vectors[label].dot(self.trigger_fh.weight_vector.toarray()[0])
        for arg in ec.getArguments():
          predicted_arg = self.classifyArgument(sentence, arg, ec, [label])
          arg_score += predicted_arg[1]
          args_guesses_by_label[label].append(label)
        dot_products[label] = dot_products[label] + arg_score

      # CASE 2 BINDING
      if label == "Binding":
        arg_score = 0
        self.trigger_fh.feature_vectors["Binding"] = self.phiTrigger(sentence, ec, "Binding")
        dot_products[label] = self.trigger_fh.feature_vectors[label].dot(self.trigger_fh.weight_vector.toarray()[0])
        for arg in ec.getArguments():
          for l_arg in ["None", "Theme"]:
            predicted_arg = self.classifyArgument(sentence, arg, ec, ["None", "Theme"])
            arg_score += predicted_arg[1]
            args_guesses_by_label[l_arg].append(predicted_arg[0])
        dot_products[label] = dot_products[label] + arg_score

      # CASE 3
      if label in ["Gene_expression", "Transcription", "Protein_catabolism", "Phosphorylation", "Localization"]:
        arg_score = 0
        self.trigger_fh.feature_vectors[label] = self.phiTrigger(sentence, ec, label)
        dot_products[label] = self.trigger_fh.feature_vectors[label].dot(self.trigger_fh.weight_vector.toarray()[0])
        args_len = len(ec.getArguments())
        l_arg_scores = dict()
        l_arg_scores["None"] = list([0] * args_len)
        l_arg_scores["Theme"] = list([0] * args_len)
        l_arg_scores["Cause"] = list([0] * args_len)

        for arg in ec.getArguments():
          counter = 0
          for l_arg in ["None", "Theme", "Cause"]:
            score = self.classifyArgument(sentence, arg, ec, [l_arg])
            l_arg_scores[l_arg][counter] = score
            counter += 1

        results_theme = list()
        results_cause = list()

        for i in range(args_len):
          results_theme[i] = l_arg_scores["Theme"][i] - l_arg_scores["None"][i]
          results_cause[i] = l_arg_scores["Cause"][i] - l_arg_scores["None"][i]

        max_theme_index, max_theme_value = max(enumerate(results_theme), key=operator.itemgetter(1))
        max_cause_index, max_cause_value = max(enumerate(results_cause), key=operator.itemgetter(1))
        if max_cause_index == max_theme_index:
          max_cause_index = results_cause.index(max(n for n in results_cause if n != max_cause_value))




  def perceptron(self, docs, max_iterations=1):
    start_time = time.time()
    start_text = "### Perceptron Started at " + time.strftime("%H:%M:%S", time.gmtime()) + " ###"
    print "#" * len(start_text)
    print start_text
    print "#" * len(start_text)
    # docs = json.getJsonDocuments(training_path)
    for i in range(0, max_iterations, 1):
      iteration_start_time = time.time()

      perceptron_doc_count = 0
      self.none_counter = 0
      for doc in docs:
        perceptron_doc_count += 1

        doc_obj = document.Document(doc)

        for sentence in doc_obj.getSentences():

          for ec in sentence.getEventCandidates():
            self.none_counter += 1

            if ec.gold != 'None' or self.none_counter % self.NONE_DOWNSAMPLE == 0:
              # Trigger Perceptron
              trigger_guess = self.classifyTrigger(sentence, ec)
              if trigger_guess != ec.gold:
                self.trigger_fh.weight_vector = (self.trigger_fh.weight_vector + self.trigger_fh.feature_vectors[ec.gold])
                self.trigger_fh.weight_vector = (self.trigger_fh.weight_vector - self.trigger_fh.feature_vectors[trigger_guess])
              if ec.gold != "None":
                # Argument Perceptron
                for arg in ec.getArguments():
                  argument_guess = self.classifyArgument(sentence, arg, ec)[0]
                  if argument_guess != arg.gold:
                    self.argument_fh.weight_vector = (self.argument_fh.weight_vector + self.argument_fh.feature_vectors[arg.gold])
                    self.argument_fh.weight_vector = (self.argument_fh.weight_vector - self.argument_fh.feature_vectors[argument_guess])
            print "Feature Vector %s" % self.trigger_fh.feature_vectors
            print "Weights %s" % self.trigger_fh.weight_vector
      iteration_end_time = time.time()
      print "%d/%d | Time: %s | Duration: %.1f min" % (i + 1, max_iterations, time.strftime("%H:%M:%S", time.gmtime()), (iteration_end_time - iteration_start_time) / 60)

    end_time = time.time()
    minutes_elapsed = "%.1f min" % ((end_time - start_time) / 60)
    end_text = "### Perceptron Finished at " + time.strftime("%H:%M:%S", time.gmtime()) + " | Total Duration {} ###".format(minutes_elapsed)
    print "\n"
    print "#" * len(end_text)
    print end_text
    print "#" * len(end_text)
    print ""
