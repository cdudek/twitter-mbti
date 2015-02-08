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
    self.word_pattern = r'(@\w+|#\w+|\w+)'
    self.url_pattern = r'(http|ftp|https):\/\/[\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&amp;:/~\+#]*[\w\-\@?^=%&amp;/~\+#])?'
    self.user = user
    self.word_count = 0
    self.tweet_pos_count = {'PRP$': 0, 'VBG': 0, 'FW': 0, '``': 0, 'VBN': 0, 'VBP': 0, 'WDT': 0, 'JJ': 0, 'WP': 0, 'VBZ': 0, 'DT': 0, 'RP': 0, 'NN': 0, 'VBD': 0, 'POS': 0, '.': 0, 'TO': 0, 'PRP': 0, 'RB': 0, ':': 0, 'NNS': 0, 'LS': 0, 'VB': 0, 'WRB': 0, 'CC': 0, 'PDT': 0, 'RBS': 0, 'RBR': 0, 'CD': 0, '-NONE-': 0, 'EX': 0, 'IN': 0, 'WP$': 0, 'MD': 0, 'NNPS': 0, 'JJS': 0, 'JJR': 0, 'SYM': 0, 'UH': 0, 'NNP': 0}
    self.profile_pos_count = {'PRP$': 0, 'VBG': 0, 'FW': 0, '``': 0, 'VBN': 0, 'VBP': 0, 'WDT': 0, 'JJ': 0, 'WP': 0, 'VBZ': 0, 'DT': 0, 'RP': 0, 'NN': 0, 'VBD': 0, 'POS': 0, '.': 0, 'TO': 0, 'PRP': 0, 'RB': 0, ':': 0, 'NNS': 0, 'LS': 0, 'VB': 0, 'WRB': 0, 'CC': 0, 'PDT': 0, 'RBS': 0, 'RBR': 0, 'CD': 0, '-NONE-': 0, 'EX': 0, 'IN': 0, 'WP$': 0, 'MD': 0, 'NNPS': 0, 'JJS': 0, 'JJR': 0, 'SYM': 0, 'UH': 0, 'NNP': 0}


  def getProfilePosCount(self):
    for tweet in self.user["user"].values():
      tokens = self.tokenizeTweet(tweet["text"])
      self.addPosToDict(tokens)


  def getPosCount(self):
    for tweet in self.user["tweets"].values():
      tokens = self.tokenizeTweet(tweet["text"])
      self.addPosToDict(tokens)



  def addPosToDict(self, tokens):
    tokens = nltk.pos_tag(tokens)
    for token in tokens:
      try:
        self.tweet_pos_count[token[1]] += 1
        self.word_count += 1
      except:
        self.tweet_pos_count[token[1]] = 1
        self.word_count += 1

  def addPosToDictProfile(self, tokens):
    tokens = nltk.pos_tag(tokens)
    for token in tokens:
      try:
        self.profile_pos_count[token[1]] += 1
      except:
        self.profile_pos_count[token[1]] = 1


  def tokenizeTweet(self, tweet):
    tweet = re.sub(self.url_pattern, 'REPLACED_URL', tweet)
    text = tweet.lower()
    # text = re.sub("", " ", text)
    # print tokenize(text)
    tokenizer = RegexpTokenizer(self.word_pattern)
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