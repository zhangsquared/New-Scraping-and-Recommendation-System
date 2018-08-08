"""Grab News Url from NewsAPI"""
import datetime
import hashlib
import logging
import redis
import os
import sys

# import common package in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

import news_api_client #pylint: disable=import-error, wrong-import-position
from cloudAMQP_client import CloudAMQPClient #pylint: disable=import-error, wrong-import-position

SLEEP_TIME_IN_SECONDS = 60 * 5
NEWS_TIME_OUT_IN_SECONDS = 3600 * 24 * 3 # 3 days

REDIS_HOST = 'localhost'
REDIS_PORT = 6379

SCRAPER_QUEUE_URL = ""
SCRAPER_QUEUE_NAME = "news-scraper-queue"

NEWS_SOURCES = [
  'bbc-news',
  'bbc-sport',
  'cnn',
  'entertainment-weekly',
  'espn',
  'ign',
  'techcrunch',
  'the-new-york-times',
  'the-wall-street-journal',
  'the-washington-post'
]

logger_format = '%(asctime)s - %(message)s'
logging.basicConfig(format=logger_format)
logger = logging.getLogger('news_monitor')
logger.setLevel(logging.DEBUG)

redis_client = redis.StrictRedis(REDIS_HOST, REDIS_PORT)
cloundAMQP_client = CloudAMQPClient(SCRAPER_QUEUE_URL, SCRAPER_QUEUE_NAME)

def run(news_api_client):
  """ fetch news from NewsAPI, 
  use redis to remove repeated, 
  send non-repeated to Scraper Queue """
  while True:
    news_list = news_api_client.getNewsFromSources(NEWS_SOURCES)

    num_of_new_news = 0
    num_of_total_news = 0

    for news in news_list:
      # or description, etc.
      # then change the string to hex
      news_digest = hashlib.md5(news['title'].encode('utf-8')).hexdigest()
      num_of_total_news += 1

      if redis_client.get(news_digest) is None:
        num_of_new_news += 1
        news['digest'] = news_digest

        if news['publishedAt'] is None:
          news['publishedAt'] = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

        redis_client.set(news_digest, '1')
        redis_client.expire(news_digest, NEWS_TIME_OUT_IN_SECONDS)

        cloundAMQP_client.sendMessage(news)

    logger.info("Fetched total %d news, including %d new news.", num_of_total_news, num_of_new_news)

    cloundAMQP_client.sleep(SLEEP_TIME_IN_SECONDS)

# redis-cli flushall

if __name__ == "__main__":
  run(news_api_client)