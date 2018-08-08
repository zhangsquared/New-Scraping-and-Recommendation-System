"""Save Non-Duplicated into MongoDB"""

import datetime
import logging
import nltk
import os
import sys
import string

from dateutil import parser
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem.porter import PorterStemmer

# import common package in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

import mongodb_client #pylint: disable=import-error, wrong-import-position
from cloudAMQP_client import CloudAMQPClient #pylint: disable=import-error, wrong-import-position
import news_topic_modeling_service_client #pylint: disable=import-error, wrong-import-position

DEDUPER_QUEUE_URL = ""
DEDUPER_QUEUE_NAME = "news-deduper-queue"

SLEEP_TIME_IN_SECONDS = 1

NEWS_TABLE_NAME = "news_list"

SAME_NEWS_SIMILARITY_THRESHOLD = 0.82

logger_format = '%(asctime)s - %(message)s'
logging.basicConfig(format=logger_format)
logger = logging.getLogger('news_deduper')
logger.setLevel(logging.DEBUG)

cloudAMQP_client = CloudAMQPClient(DEDUPER_QUEUE_URL, DEDUPER_QUEUE_NAME)

stemmer = PorterStemmer()
translator = str.maketrans('','',string.punctuation)

def stem_tokens(tokens, stemmer):
  stemmed = []
  for item in tokens:
    stemmed.append(stemmer.stem(item))
  return stemmed

def tokenize(text):
  tokens = nltk.word_tokenize(text)
  stems = stem_tokens(tokens, stemmer)
  return stems

def process_document(documents):
  """case-insensitive, remove puctuation"""
  rtn = []
  for doc in documents:
    no_punctuation = doc.lower().translate(translator)
    rtn.append(no_punctuation)
  return rtn



def handle_message(msg):
  if not isinstance(msg, dict):
    print('message is broken')
    return
  
  text = msg['text']
  if text is None: 
    logger.warning('text is none')
    return
  
  published_at = parser.parse(msg['publishedAt'])
  published_at_day_begin = datetime.datetime(published_at.year, published_at.month, published_at.day, 0, 0, 0, 0)
  published_at_day_end = published_at_day_begin + datetime.timedelta(days=1)

  db = mongodb_client.get_db()
  same_day_news_list = list(db[NEWS_TABLE_NAME].find({
      'publishedAt': {
        '$gte': published_at_day_begin,
        '$lt': published_at_day_end
      }
    }))

  if same_day_news_list is not None and len(same_day_news_list) > 0:
    documents = [news['text'] for news in same_day_news_list]
    documents.insert(0, text)

    # add tokenizer and stemmer
    tfidf = TfidfVectorizer(tokenizer = tokenize)
    processed_document = process_document(documents)
    tfs = tfidf.fit_transform(processed_document)
    pairwise_sim = tfs * tfs.T
    # logger.debug("Pairwise Sim:%s", str(pairwise_sim))
    rows, _ = pairwise_sim.shape
    maxSim = -1
    for row in range(1, rows):
      if pairwise_sim[row, 0] > maxSim:
          maxSim = pairwise_sim[row, 0]
      if pairwise_sim[row, 0] > SAME_NEWS_SIMILARITY_THRESHOLD:        
        logger.info("Duplicated news. Ignore. Similarity: %.6f" %pairwise_sim[row, 0])
        return
    logger.info("Find one new news. Largest similarity: %.6f among %d news", maxSim, len(same_day_news_list))
  else:
    logger.info("Find one new news. No same day news.")
   
  msg['publishedAt'] = parser.parse(msg['publishedAt'])

  description = msg['description']
  if description is None:
    description = msg['title']
  
  topic = news_topic_modeling_service_client.classify(description)
  # for every new news, it will add the label class before saved into db
  msg['class'] = topic

  # update or insert
  db[NEWS_TABLE_NAME].replace_one({ 'digest': msg['digest'] }, msg, upsert=True)

def run():
  while True:
    if cloudAMQP_client is not None:
      msg = cloudAMQP_client.getMessage()
      if msg is not None:
        # Parse and process the message
        try:
          handle_message(msg)
        except Exception as e:
          logger.warning(e)
          pass

      cloudAMQP_client.sleep(SLEEP_TIME_IN_SECONDS)


if __name__ == "__main__":
  run()
