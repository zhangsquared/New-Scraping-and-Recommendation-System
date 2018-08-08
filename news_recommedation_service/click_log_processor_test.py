import click_log_processor
import os
import sys
from datetime import datetime

NUM_OF_CLASSES = 8

PREFERENCE_TABLE_NAME= "user_preference_model"

USERID = 'user1'
NEWSID = '806dc827b5db6d4f283ea4dfabe0e0af'

import news_classes

# import common package in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
import mongodb_client #pylint: disable=import-error, wrong-import-position

def test_basic():
  db = mongodb_client.get_db()
  db[PREFERENCE_TABLE_NAME].delete_many({ 'userId': USERID })

  msg = {'userId': USERID, 'newsId': NEWSID, 'timestamp': str(datetime.utcnow())}

  click_log_processor.handle_message(msg)

  model = db[PREFERENCE_TABLE_NAME].find_one({'userId': USERID})

  assert model is not None
  assert len(model['preference']) == NUM_OF_CLASSES
  print("test_basic passed!")

if __name__ == "__main__":
  test_basic()

