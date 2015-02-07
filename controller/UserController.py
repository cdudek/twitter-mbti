__author__ = 'calvindudek'
from TwitterHandler import TwitterHandler
import re

class UserController:
  def __init__(self):
    self.users = []
    self.twitter_handler = TwitterHandler()

  def getUsersBySearchTerm(self, query):
    search_results = self.twitter_handler.search(query)
    users = list()
    for post in search_results:
      users.append(post._json["user"]["screen_name"])
    # print users
    return users

  def getFollowers(self, name):
      users = []
      follower_ids = self.twitter_handler.getFollowers(name)
      print len(follower_ids)
      for id in follower_ids:
          print "hi"
          name = self.twitter_handler.api.get_user(id).screen_name
          print name
          users.append(name)
      return users

  def getUsersBySearchTermRules(self, query):


    search_results = self.twitter_handler.search(query)
    users = list()
    for post in search_results:
      text = post._json["text"].lower()
      text = re.sub("[^\\w\\s\\-\\<.*?>]", " ", text)
      tokens = text.split(" ")
      num_type_words = self.getNumberOfTypeWords(tokens)
      num_pronouns = self.getNumberOfPronouns(tokens)


      if num_type_words == 1 and num_pronouns > 0:
        users.append(post._json["user"]["screen_name"])
    # print users
    return users

  def getNumberOfTypeWords(self, tokens):
    keywords = ["enfj", "enfp", "entj", "entp", "esfj", "esfp", "estj", "estp", "infj", "infp", "intji", "ntp", "isfj", "isfp", "istj", "istp"]
    count = 0
    for token in tokens:
      if token in keywords:
        count += 1
    return count

  def getNumberOfPronouns(self, tokens):
    keywords = ["i", "my", "did"]
    count = 0
    for token in tokens:
      if token in keywords:
        count += 1
    return count

  def getUser(self, screen_name):
    pass