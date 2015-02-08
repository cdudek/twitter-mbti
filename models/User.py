__author__ = 'calvindudek'
import json
from TwitterHandler import TwitterHandler

class User:
  def __init__(self, screen_name, mbti_type):
    self.screen_name = screen_name
    self.properties = {}
    self.tweets = {}
    self.twitter_handler = TwitterHandler()
    self.user_timeline = self.twitter_handler.getUserTimeline(screen_name)
    self.valid = self.user_timeline
    self.mbti_type = mbti_type

    for status in self.user_timeline:
      status = status._json
      if self.properties == {}:
        self.setProperties(status["user"])
      status.pop("user")
      self.tweets[status["id"]] = status

  def getUserAsJson(self):
    return {"user": self.properties, "tweets": self.tweets, "mbti type": self.mbti_type}

  def readTweets(self, timeline):
    results = {}
    for status in timeline:
      status = status._json
      status.pop("user")
      # print status
      results[status["id"]] = status


    return results

  def setProperties(self, user):
    # print user
    # if user["screen_name"] == self.screen_name[1:]:
    self.properties = user


  def writeFile(self):
    file_name = "data/" + self.mbti_type + "_"+ self.screen_name[0:] + ".json"
    file = open(file_name, "w")
    json.dump(self.getUserAsJson(), file, indent=2)
