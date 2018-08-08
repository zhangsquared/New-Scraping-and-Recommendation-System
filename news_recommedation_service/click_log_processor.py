# -*- coding: utf-8 -*-

'''
Time decay mode:

If selected:
p = (1-a)p + a

If not:
p = (1-a)p

Where p is the selection prob, and a is the degree of weight decrease.
The result of this is that the nth most recent selection will have a weight of 
(1-a)^n. Useing a coefficient value of 0.05 as an example, the 10th most recent
selection would only have half the weight of the most recent. Increasing epsilon 
would bias towards most recent results more.
'''

import logging
import os
import sys

NUM_OF_CLASSES = 8
INIT_P = 1.0 / NUM_OF_CLASSES
ALPHA = 0.1

SLEEP_TIME_IN_SEC = 1

PREFERENCE_TABLE_NAME= "user_preference_model"
NEWS_TABLE_NAME = 'news'

import news_classes

# import common package in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
from cloudAMQP_client import CloudAMQPClient #pylint: disable=import-error, wrong-import-position
CLICK_QUEUE_URL = ""
ClICK_QUEUE_NAME = "news-click-queue"
click_client = CloudAMQPClient(CLICK_QUEUE_URL, ClICK_QUEUE_NAME)

import mongodb_client #pylint: disable=import-error, wrong-import-position

LOGGER_FORMAT = '%(asctime)s - %(message)s'
logging.basicConfig(format = LOGGER_FORMAT)
LOGGER = logging.getLogger('click_log_processor')
LOGGER.setLevel(logging.DEBUG)


def handle_message(msg):
  if not isinstance(msg, dict):
    return
  
  if ('userId' not in msg
    or 'newsId' not in msg
    or 'timestamp' not in msg):
    return
  
  user_id = msg['userId']
  news_id = msg['newsId']

  # update user preference
  db = mongodb_client.get_db()
  model = db[PREFERENCE_TABLE_NAME].find_one({'userId': user_id})

  if model is None:
    LOGGER.info('Creating preference model for new user: %s', user_id)
    new_model = {'userId': user_id}
    preference = {}
    for i in news_classes.classes:
      preference[i] = float(INIT_P)
    new_model['preference'] = preference
    model = new_model
  
  LOGGER.info('Updating preference model for user %s', user_id)

  # update model using time decying method
  news = db[NEWS_TABLE_NAME].find_one({'digest': news_id})

  # news should have 'class' field
  # and the class should be in the news_class list
  if news is None:
    LOGGER.info('there is no news with digest: '+ news_id)
    return
  if 'class' not in news:
    LOGGER.info('there is no class for news.')
    return
  if news['class'] not in news_classes.classes:
    LOGGER.info('do not have a valid class: ' + news['class'])
    return

  click_class = news['class']
  # update the clicked one
  old_p = model['preference'][click_class]
  model['preference'][click_class] = float((1 - ALPHA) * old_p + ALPHA)
  # update note clied classes
  for i, _ in model['preference'].items():
    if not i == click_class:
      model['preference'][i] = float((1 - ALPHA) * model['preference'][i])
    
  db[PREFERENCE_TABLE_NAME].replace_one({'userId': user_id}, model, upsert=True)


def run():
  while(True):
    if click_client is not None:
      msg = click_client.getMessage()
      if msg is not None:
        try:
          handle_message(msg)
        except Exception as e:
          LOGGER.warn(e)
          pass
      click_client.sleep(SLEEP_TIME_IN_SEC)

if __name__ == "__main__":
  run()
