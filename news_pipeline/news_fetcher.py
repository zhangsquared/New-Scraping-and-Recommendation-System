"""Extract News Content"""
import logging
import os
import sys

from newspaper import Article

# import common package in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'scrapers', ))

from cloudAMQP_client import CloudAMQPClient #pylint: disable=import-error, wrong-import-position
import cnn_news_scraper #pylint: disable=import-error, wrong-import-position

SCRAPER_QUEUE_URL = ""
SCRAPER_QUEUE_NAME = "news-scraper-queue"

DEDUPER_QUEUE_URL = ""
DEDUPER_QUEUE_NAME = "news-deduper-queue"

SLEEP_TIME_IN_SECONDS = 5

logger_format = '%(asctime)s - %(message)s'
logging.basicConfig(format=logger_format)
logger = logging.getLogger('news_fetcher')
logger.setLevel(logging.DEBUG)

scrape_queue_client = CloudAMQPClient(SCRAPER_QUEUE_URL, SCRAPER_QUEUE_NAME)
dedupe_queue_client = CloudAMQPClient(DEDUPER_QUEUE_URL, DEDUPER_QUEUE_NAME)

def handle_message_old(msg):
  # if the msg is not json format
  if not isinstance(msg, dict):
    logger.warning('message is broken')
    return
  
  text = None
  if msg['source'] == 'cnn':
    text = cnn_news_scraper.extract_news(msg['url'])

  if text is not None and len(text) > 0:
    msg['text'] = text
    dedupe_queue_client.sendMessage(msg)


def handle_message(msg):
  # if the msg is not json format
  if not isinstance(msg, dict):
    logger.warning('message is broken')
    return
  
  text = fetch(msg['url'])

  if text is not None and len(text) > 0:
    msg['text'] = text
    dedupe_queue_client.sendMessage(msg)

def fetch(url):
  article = Article(url)
  article.download()
  article.parse()

  text = article.text
  return text

def run():
  """get news url from Scraper Queue
  use Scraper to extract message
  send extacted text into deduper Queue"""
  while True:
    if scrape_queue_client is not None:
      msg = scrape_queue_client.getMessage()

      if msg is not None:
        try:
          handle_message(msg)
        except Exception as e:
          logger.warning(e)
          pass
        scrape_queue_client.sleep(SLEEP_TIME_IN_SECONDS)

if __name__ == "__main__":
    run()
