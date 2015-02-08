__author__ = 'calvindudek'

import nltk
from os import listdir
from os.path import isfile, join
import json
import re
from tokenize import tokenize
import nltk
from nltk.tokenize import RegexpTokenizer


class NLP():
  def __init__(self, user):
    # self.word_counts = dict()
    self.__word_pattern = r'(@\w+|#\w+|\w+)'
    self.__url_pattern = r'(http|ftp|https):\/\/[\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&amp;:/~\+#]*[\w\-\@?^=%&amp;/~\+#])?'
    self.__user = user
    self.tweet_word_count = 0.0
    self.tweet_word_count_by_pos = {'PRP$': 0.0, 'VBG': 0.0, 'FW': 0.0, '``': 0.0, 'VBN': 0.0, 'VBP': 0.0, 'WDT': 0.0, 'JJ': 0.0, 'WP': 0.0, 'VBZ': 0.0, 'DT': 0.0, 'RP': 0.0, 'NN': 0.0, 'VBD': 0.0, 'POS': 0.0, '.': 0.0, 'TO': 0.0, 'PRP': 0.0, 'RB': 0.0, ':': 0.0, 'NNS': 0.0, 'LS': 0.0, 'VB': 0.0, 'WRB': 0.0, 'CC': 0.0, 'PDT': 0.0, 'RBS': 0.0, 'RBR': 0.0, 'CD': 0.0, '-NONE-': 0.0, 'EX': 0.0, 'IN': 0.0, 'WP$': 0.0, 'MD': 0.0, 'NNPS': 0.0, 'JJS': 0.0, 'JJR': 0.0, 'SYM': 0.0, 'UH': 0.0, 'NNP': 0.0}
    self.profile_word_count = 0.0
    self.profile_word_count_by_pos = {'PRP$': 0.0, 'VBG': 0.0, 'FW': 0.0, '``': 0.0, 'VBN': 0.0, 'VBP': 0.0, 'WDT': 0.0, 'JJ': 0.0, 'WP': 0.0, 'VBZ': 0.0, 'DT': 0.0, 'RP': 0.0, 'NN': 0.0, 'VBD': 0.0, 'POS': 0.0, '.': 0.0, 'TO': 0.0, 'PRP': 0.0, 'RB': 0.0, ':': 0.0, 'NNS': 0.0, 'LS': 0.0, 'VB': 0.0, 'WRB': 0.0, 'CC': 0.0, 'PDT': 0.0, 'RBS': 0.0, 'RBR': 0.0, 'CD': 0.0, '-NONE-': 0.0, 'EX': 0.0, 'IN': 0.0, 'WP$': 0.0, 'MD': 0.0, 'NNPS': 0.0, 'JJS': 0.0, 'JJR': 0.0, 'SYM': 0.0, 'UH': 0.0, 'NNP': 0.0}

    self.__getPosProfileWordCount()
    self.__getPosWordCount()



  def __getPosProfileWordCount(self):
    # for user in self.__user["user"]:
    # print user
    description = self.__user["user"]["description"]

    if description != "":
      # print description
      tokens = self.__tokenizeTweet(description)
      self.__addPosToDictProfile(tokens)


  def __getPosWordCount(self):
    for tweet in self.__user["tweets"].values():
      tokens = self.__tokenizeTweet(tweet["text"])
      self.__addPosToDict(tokens)

  def getPosDescriptionDist(self):
    results = list()
    for val in self.profile_word_count_by_pos.values():
      # print val
      try:
        results.append(val/self.profile_word_count)
      except:
        results.append(0.0)

    return results

  def getPosTweetDist(self):
    results = list()
    for val in self.tweet_word_count_by_pos.values():
      results.append(val/self.tweet_word_count)
    return results

  def __addPosToDict(self, tokens):
    tokens = nltk.pos_tag(tokens)
    for token in tokens:
      try:
        self.tweet_word_count_by_pos[token[1]] += 1.0
        self.tweet_word_count  += 1.0
      except:
        self.tweet_word_count_by_pos[token[1]] = 1.0
        self.tweet_word_count  += 1.0


  def __addPosToDictProfile(self, tokens):
    tokens = nltk.pos_tag(tokens)
    # print tokens
    for token in tokens:
      try:
        self.profile_word_count_by_pos[token[1]] += 1.0
        self.profile_word_count += 1.0
      except:
        self.profile_word_count_by_pos[token[1]] = 1.0
        self.profile_word_count += 1.0


  def __tokenizeTweet(self, tweet):
    tweet = re.sub(self.__url_pattern, 'REPLACED_URL', tweet)
    text = tweet.lower()
    # text = re.sub("", " ", text)
    # print tokenize(text)
    tokenizer = RegexpTokenizer(self.__word_pattern)
    tokens = tokenizer.tokenize(text)
    # nltk.ngrams(tokens, 1):
    # print tokens
    # return text.split(" ")
    return tokens

  # def addWordToDict(self, word):
  #   try:
  #     self.word_counts[word] += 1
  #   except:
  #     self.word_counts[word] = 1
  #   # print self.word_counts

  # def getFiles(self):
  #   # print self.path
  #   results = list()
  #   files = [f for f in listdir(self.path) if isfile(join(self.path, f))]
  #   for file in files:
  #     if(file.endswith(".json")):
  #       json_file = json.loads(open(self.path + file).read())
  #       results.append(json_file)
  #   return results


# POS TAGS
#
# Number
# Tag
# # Description
# CC	Coordinating conjunction
# CD	Cardinal number
# DT	Determiner
# EX	Existential there
# FW	Foreign word
# IN	Preposition or subordinating conjunction
# JJ	Adjective
# JJR	Adjective, comparative
# JJS	Adjective, superlative
# LS	List item marker
# MD	Modal
# Noun, singular or mass
# NNS	Noun, plural
# NNP	Proper noun, singular
# NNPS	Proper noun, plural
# PDT	Predeterminer
# POS	Possessive ending
# PRP	Personal pronoun
# PRP$	Possessive pronoun
# RB	Adverb
# RBR	Adverb, comparative
# RBS	Adverb, superlative
# RP	Particle
# SYM	Symbol
# TO	to
# UH	Interjection
# VB	Verb, base form
# VBD	Verb, past tense
# VBG	Verb, gerund or present participle
# VBN	Verb, past participle
# VBP	Verb, non-3rd person singular present
# VBZ	Verb, 3rd person singular present
# WDT	Wh-determiner
# WP	Wh-pronoun
# WP$	Possessive wh-pronoun
# WRB	Wh-adverb