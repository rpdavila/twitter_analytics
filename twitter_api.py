import os
import tweepy
import mariadb
import datetime

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

# store data into db table twitter_trends_available
def store_data(trend_name, trend_woeid):
    try:
        conn = mariadb.connect(
            user=os.getenv("mariadb_user"),
            password=os.getenv("mariadb_pass"),
            host="192.168.1.5",
            port=3306,
            database="twitter"
        )

        cur = conn.cursor()
        insert_query = 'INSERT INTO twitter.twitter_trends_available(country, woeid) VALUES (?,?)'
        cur.execute(insert_query, (trend_name, trend_woeid))
        conn.commit()
        conn.close()
    except mariadb.Error as e:
        print(e)

# main function to retreive data from the table twitter_trends_available grab the trends and store into twitter trends table
def retrieve_data():
    try:
        conn = mariadb.connect(
            user=os.getenv("mariadb_user"),
            password=os.getenv("mariadb_pass"),
            host="192.168.1.5",
            port=3306,
            database="twitter"
        )

        cur = conn.cursor()
        retrieve_data_worldwide = "SELECT * FROM twitter.twitter_trends_available WHERE woeid='1'"
        cur.execute(retrieve_data_worldwide)
        for country, woeid in cur:
            woeid = woeid
            country = country
            get_twitter_trends_in_specific_locations(country, woeid)
    except mariadb.Error as e:
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
            conn = mariadb.connect(
                user=os.getenv("mariadb_user"),
                password=os.getenv("mariadb_pass"),
                host="192.168.1.5",
                port=3306,
                database="twitter"
            )

            cur = conn.cursor()
            insert_query = 'INSERT INTO twitter.twitter_trends(country, name, url, query, tweet_volume, date) VALUES (?,?,?,?,?,?)'
            cur.execute(insert_query, (country, name, url, query, volume, date))
            conn.commit()
            conn.close()
        except mariadb.Error as e:
            print(e)
Print(Done!)
# uncomment the below function to pull Country and country Id of available trends in twitter
# trends_available()
# uncomment funtion below to pull trending data from twitter Worldwide ID
# retrieve_data()
