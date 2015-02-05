import json

from TwitterHandler import TwitterHandler as th
from JsonHandler import getJsonDocuments
import time
import os
import random

class TwitterUtil():
  def __init__(self):
    self.th = th()
    self.api = th().api


  def getTweet(self, tweet):


    created_at = tweet["created_at"].encode("utf-8")
    screen_name = tweet["user"]["screen_name"].encode("utf-8")
    uid = tweet["user"]["id"]
    location = tweet["user"]["location"]
    text = tweet["text"].encode("utf-8")
    description = tweet["user"]["description"]
    tid = tweet["id"]
    verified = tweet["user"]["verified"]
    statuses_count = tweet["user"]["statuses_count"]
    retweet_count = tweet["retweet_count"]
    retweeted = tweet["retweeted"]
    followers_count = tweet["user"]["followers_count"]
    try:
      place = tweet["place"]["country_code"]
    except:
      place = None
    lang = tweet["user"]["lang"]
    tweet = {"tid": tid, "created_at": created_at, "screen_name": screen_name,
             "uid": uid, "text": text, "place": place, "lang": lang, "description": description,
             "location": location, "verified": verified, "followers_count": followers_count,
             "statuses_count": statuses_count, "retweet_count": retweet_count, "retweeted":retweeted}

    return tweet

  def getUserTimeline(self, screen_name):
    statuses = self.th.getUserTimeline(screen_name, 1)
    tweet_list = list()
    for status in statuses:
      tweet = self.getTweet(status._json)
      tweet_list.append(tweet)
    return tweet_list


  def getAndSaveUserTimelineToFile(self, screen_name, file_path):
    tweets = self.getUserTimeline(screen_name)
    for tweet in tweets:
      print tweet
    self.appendToFile(tweets, file_path)



  def shortenTweets(self, statuses):
    tweet_list = []
    for status in statuses:
      try:
        tweet = self.getTweet(status._json)
        tweet_list.append(tweet)
      except:
        pass
    return tweet_list

  # def getJsonFiles(self, path):
  #   files = self.getFiles(path)
  #   json_files = list()
  #   for file in files:
  #     json_data = open(file).read()
  #     data = json.loads(json_data, encoding="utf-8")
  #     json_files.append(data)
  #   return json_files

  def getTimelinesForAllUserTweets(self, read_path, write_path, searches=1):
    files = getJsonDocuments(read_path)
    # print files
    counter = 0
    random.shuffle(files)
    for file in files:
      # random.shuffle(file)
      for tweet in file[:100]:
        # print tweet
        file_path = write_path + tweet['screen_name'].replace(" ", "_") + ".json"
        if not os.path.exists(file_path):
          start_time = time.time()
          print "%d\%d | %s | %s" % (counter, len(files), tweet['screen_name'], tweet['text'])
          results  = self.th.getUserTimeline(tweet['screen_name'], searches)
          tweets = self.shortenTweets(results)

          end_time = time.time()
          time_passed = (end_time - start_time)
          # if time_passed < 1.0 * searches:
          #   delay = (1.0 * searches) - time_passed
          #   time.sleep(delay)

          self.appendToFile(tweets, file_path)
      counter += 1


  def getFiles(self, path, file_ending=".json"):
    files = list()
    for f in os.walk(path):
      for file in f[2]:
        if(file.endswith(file_ending)):
          files.append(path + file)
    return files

  def changeFiles(self, path):
    files = self.getFiles(path)
    for file in files:
      with open(file,'r+') as f:
        content = f.read()

      name = open(file, 'a').name
      file_path = ("./new/" + name).replace("./search_results/", "")
      # print file_path

      with open(file_path, 'a') as f:
        # f.write("{\n[\n{")
        f.write(content.replace("}{", "}, {").replace('{\n[\n{', "[\n{\""))
        # f.write("\n")
        f.seek(0,0)
        f.write("")




def appendToFile(self, tweets, file_path):
  file = open(file_path, 'w')
  json.dump(tweets, file, indent=2, separators=(',', ': '))