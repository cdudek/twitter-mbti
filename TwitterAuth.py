__author__ = 'calvindudek'

import tweepy

class TwitterAuth:
  def getApi(self):
    access_token = "55683210-35aTrpN02komPhXKLJ1Ng3fo4ErhVi4HsZ6HOjrO0"
    access_token_secret = "gupCyWT3oAE5ruUGVkc7ZxwAfKedQz9mbOnpXAA6IYLST"
    consumer_key = "fuGlcYzJQhMKsX3Bw9n3Nae83"
    consumer_secret = "dOuYsm4AE15fETd2FOu6p8YdpedtE2d4kAnGMt0ipM7YV7yCC7"
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    return tweepy.API(auth,retry_count=3,retry_delay=5,retry_errors=set([401, 404, 500, 503]),wait_on_rate_limit_notify=True,wait_on_rate_limit=False,timeout=1)