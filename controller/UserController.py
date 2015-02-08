__author__ = 'calvindudek'
from TwitterHandler import TwitterHandler
import re
import os
import json

loaded_followers = 200

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
      i = 0
      for id in follower_ids:
          name = self.twitter_handler.api.get_user(id).screen_name
          print name
          users.append(name)
          if i < loaded_followers:
              i += 1
          else:
              break
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

  

  def getFiles(filepath):
    files = list()
    for f in os.walk(filepath):
      for file in f[2]:
        if(file.endswith(".json")):
          fn = filepath + file
          json_file = json.load(fn.read)
          files.append(fn.read())
    return files

  def getJsonDocuments(path):
    json_files = list()
    # files = getFiles(path)
    # for file in files:
    #   with open(file) as json_file:
    #     jsonfile = json.loads(json_file.read())
    #     json_files.append(jsonfile)
    return json_files
