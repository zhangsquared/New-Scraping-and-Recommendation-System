import json
import os
import pickle
import redis
import sys

from bson.json_util import dumps
from datetime import datetime

# import common packages in parent directory.
# add the utils into the path where python will serach the package from 
# https://api.mongodb.com/python/current/installation.html
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
import mongodb_client #pylint: disable=import-error, wrong-import-position
import news_recommendation_service_client #pylint: disable=import-error, wrong-import-position

# import common package in parent directory
from cloudAMQP_client import CloudAMQPClient #pylint: disable=import-error, wrong-import-position
CLICK_QUEUE_URL = ""
ClICK_QUEUE_NAME = "news-click-queue"
click_client = CloudAMQPClient(CLICK_QUEUE_URL, ClICK_QUEUE_NAME)

REDIS_HOST = "localhost"
REDIS_PORT = 6379

NEWS_LIST_BATCH_SIZE = 10
NEWS_LIMIT = 200
USER_NEWS_TIMEOUT_IN_SECONDS = 60 * 60 # one hour

# mongoimport --db tap_news_dev --collection news --drop --file ~/downloads/demo_news.json
NEWS_TABLE_NAME = "news"

redis_client = redis.StrictRedis()

def getOneNews():
    db = mongodb_client.get_db()
    news = db[NEWS_TABLE_NAME].find_one()
    return json.loads(dumps(news))

def getNewsSummariesForUser(user_id, page_num):
    page_num = int(page_num)
    if page_num <= 0:
        return []

    begin_index = (page_num - 1) * NEWS_LIST_BATCH_SIZE
    end_index = page_num * NEWS_LIST_BATCH_SIZE

    sliced_news = []
    db = mongodb_client.get_db()

    if redis_client.get(user_id) is not None:
        news_digests = pickle.loads(redis_client.get(user_id))
        sliced_news_digests = news_digests[begin_index:end_index]       
        sliced_news = list(db[NEWS_TABLE_NAME].find({'digest':{'$in':sliced_news_digests}}))
    else:
        total_news = list(db[NEWS_TABLE_NAME].find().sort([('publishedAt', -1)]).limit(NEWS_LIMIT))

        total_news_digests = [x['digest'] for x in total_news]
        redis_client.set(user_id, pickle.dumps(total_news_digests))
        redis_client.expire(user_id, USER_NEWS_TIMEOUT_IN_SECONDS)

        sliced_news = total_news[begin_index:end_index]
    
    # get preference for the user
    preference = news_recommendation_service_client.getPreferenceForUser(user_id)
    topPreference = None

    if preference is not None and len(preference) > 0:
        topPreference = preference[0]

    for news in sliced_news:
        # remove text field to save bandwidth
        del news['text']
        # add recommended tag to the top choices
        if (topPreference is not None 
            and 'class' in news
            and news['class'] == topPreference):
            news['reason'] = 'recommended'
 
    return json.loads(dumps(sliced_news))

def logNewsClickForUser(user_id, news_id):
    message = {
        'userId': user_id, 
        'newsId': news_id, 
        'timestamp': str(datetime.utcnow())
        }
    # Send log message to click log processor
    click_client.sendMessage(message)
