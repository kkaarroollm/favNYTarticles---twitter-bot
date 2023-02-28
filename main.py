import requests
from datetime import datetime
import tweepy
import configparser

config = configparser.ConfigParser()
config.read('/Users/karolmarszalek/app/config.ini')

nyt_api_key = config ['twitter']['nyt_api']
api_key = config['twitter']['api_key']
api_secret_key = config['twitter']['api_secret_key']
access_token = config['twitter']['access_token']
secret_access_token = config['twitter']['secret_access_token']
bearer_token = config['twitter']['bearer_token']
client_id = config['twitter']['client_id']
client_server = config['twitter']['client_server']
user_id = config['twitter']['user_id']

client = tweepy.Client(bearer_token, api_key, api_secret_key, access_token, secret_access_token)

auth = tweepy.OAuthHandler(api_key, api_secret_key)
auth.set_access_token(access_token, secret_access_token)
api = tweepy.API(auth)

# Fetching most viewed article URLs from NYT API
def fetch_most_viewed_urls():
    response = requests.get(f'https://api.nytimes.com/svc/mostpopular/v2/viewed/1.json?api-key={nyt_api_key}').json()
    return [article['url'] for article in response['results']]

most_viewed_urls = fetch_most_viewed_urls()

# Filtering out previously published articles from Twitter account
def filter_published_tweets(user_id, urls):
    published_urls = set()
    tweets = api.user_timeline(user_id=user_id, count=200, tweet_mode='extended')
    for tweet in tweets:
        for url in tweet.entities['urls']:
            if url['url'].startswith('https://'):
                published_urls.add(requests.get(url['url']).url)
    return list(set(urls) - published_urls)

filtered_urls = filter_published_tweets(user_id, most_viewed_urls)

# Posting new article URL to Twitter
if filtered_urls:
    now = datetime.now()
    dt_string = now.strftime("%B %d")
    tweet_text = f'Today is {dt_string}, and this is the most viewed article on The New York Times: {filtered_urls[0]}'
    client.create_tweet(text=tweet_text)

