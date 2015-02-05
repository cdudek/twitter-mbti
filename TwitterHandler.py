__author__ = 'calvindudek'

from TwitterAuth import TwitterAuth
import sys
import time
import jsonpickle
# from models.User import User
import json


class TwitterHandler:
  def __init__(self):
    self.api = TwitterAuth().getApi()

  def search(self, query, n=1):
    statuses = self.api.search(q=query, lang='en', count=100,result_type="")
    # tweet_list = dict()
    # count = 1
    # for status in statuses:
    #   print count
    #   tweet = self.minimizeTweet(status._json)
    #   tweet_list[tweet["screen_name"]] = tweet
    #   count += 1
    return statuses

  def getUser(self, screen_name):
    user = self.api.get_user(screen_name)
    return user

  def getUserTimeline(self, screen_name):
    return self.api.user_timeline(screen_name, count=200)



  def minimizeTweet(self, tweet):
    result = {}

    result["created_at"] = tweet["created_at"].encode("utf-8")
    result['screen_name'] = tweet["user"]["screen_name"].encode("utf-8")
    result['uid'] = tweet["user"]["id"]
    result['location'] = tweet["user"]["location"]
    result['text'] = tweet["text"].encode("utf-8")
    result['description'] = tweet["user"]["description"]
    result['tid'] = tweet["id"]
    result['verified'] = tweet["user"]["verified"]
    result['statuses_count'] = tweet["user"]["statuses_count"]
    result['retweet_count'] = tweet["retweet_count"]
    result['retweeted'] = tweet["retweeted"]
    result['followers_count'] = tweet["user"]["followers_count"]
    return result

