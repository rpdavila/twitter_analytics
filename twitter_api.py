import os
import tweepy
import mariadb
import sys
import time

consumer_key = os.getenv("twitter_consumer_key")
secret_key = os.getenv("twitter_secret_key")
access_token = os.getenv("twitter_access_token")
secret_token = os.getenv("twitter_secret_access_token")

auth = tweepy.OAuthHandler(consumer_key, secret_key)
auth.set_access_token(access_token, secret_token)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

# connect to db
try:
    conn = mariadb.connect(
        user=os.getenv("mariadb_user"),
        password=os.getenv("mariadb_pass"),
        host="192.168.1.5",
        port=3306,
        database="twitter"
    )
    cur = conn.cursor()
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)


# Function that grabs the name and country id of trending data
def trends_avail():
    trending = api.trends_available()
    for trend in trending:
        trend_name = trend['name']
        trend_woeid = trend['woeid']
        store_data(trend_name, trend_woeid)


def store_data(trend_name, trend_woeid):
    try:
        insert_query = 'INSERT INTO twitter.twitter_trends_available(name, woeid) VALUES (?,?)'
        cur.execute(insert_query, (trend_name, trend_woeid))
        conn.commit()
        conn.close()
    except mariadb.Error as e:
        print(e)


trends_avail()
