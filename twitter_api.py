import os
import tweepy
import time

consumer_key = os.getenv("twitter_consumer_key")
secret_key = os.getenv("twitter_secret_key")
access_token = os.getenv("twitter_access_token")
secret_token = os.getenv("twitter_secret_access_token")

auth = tweepy.OAuthHandler(consumer_key, secret_key)
auth.set_access_token(access_token, secret_token)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

trending = api.trends_available()


# Function that grabs the name and country of trending data
def trends_avail():
    for trend in trending:
        print(trend['name'], trend['woeid'])
