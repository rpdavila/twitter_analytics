import os
import tweepy
import datetime
import sqlite3
from sqlite3 import Error

consumer_key = os.getenv("twitter_consumer_key")
secret_key = os.getenv("twitter_secret_key")
access_token = os.getenv("twitter_access_token")
secret_token = os.getenv("twitter_secret_access_token")

auth = tweepy.OAuthHandler(consumer_key, secret_key)
auth.set_access_token(access_token, secret_token)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


# Function that grabs the name and country id of trending data
def trends_available():
    trending = api.trends_available()
    for trend in trending:
        trend_name = trend['name']
        trend_woeid = trend['woeid']
        store_data(trend_name, trend_woeid)


# store data into db table twitter_trends_available which will grab the country name and country id
def store_data(trend_name, trend_woeid):
    try:
        conn = sqlite3.connect('db.sqlite')
        cur = conn.cursor()
        insert_query = 'INSERT OR Ignore INTO main.country_id(country, woeid) VALUES (?,?)'
        cur.execute(insert_query, (trend_name, trend_woeid))
        conn.commit()
        conn.close()
    except Error as e:
        print(e)


"""
Main function to retrieve data from the table twitter_trends_available. It will grab the trends 
and store it into twitter trends table
"""


def retrieve_data(field_data):
    try:
        conn = sqlite3.connect('db.sqlite')
        cur = conn.cursor()
        get_data = f"SELECT woeid FROM country_id WHERE country='{field_data}'"
        cur.execute(get_data)
        for woeid in cur:
            woeid = woeid[0]
            country = field_data
            get_twitter_trends_in_specific_locations(country, woeid)
    except Error as e:
        print(e)


def get_twitter_trends_in_specific_locations(country, woeid):
    try:
        trending_places = api.trends_place(woeid)
        for data in trending_places:
            for trends in data['trends']:
                name = trends['name']
                url = trends['url']
                query = trends['query']
                volume = trends['tweet_volume']
                date = datetime.datetime.now()
                insert_data_into_twitter_trends(country, name, url, query, volume, date)
    except tweepy.TweepError as e:
        print(e.reason)


def insert_data_into_twitter_trends(country, name, url, query, volume, date):
    try:
        conn = sqlite3.connect('db.sqlite')
        cur = conn.cursor()
        insert_query = 'INSERT INTO main.twitter_trends(country, name, url, query, volume, date)' \
                       'VALUES(?,?,?,?,?,?)'
        cur.execute(insert_query, (country, name, url, query, volume, date))
        conn.commit()
        conn.close()
    except Error as e:
        print(e)


def get_name_volume():
    try:
        conn = sqlite3.connect('db.sqlite')
        curs = conn.cursor()
        query = "SELECT name,volume FROM main.twitter_trends ORDER BY volume DESC"
        curs.execute(query)
        return curs.fetchall()
    except Error as e:
        print(e)
