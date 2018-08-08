# http://api.mongodb.com/python/current/tutorial.html
from pymongo import MongoClient

MONGO_DB_HOST = 'localhost'
MONGO_DB_PORT = 27017 # default port
DB_NAME  = 'tap_news_dev' # dtaabase name, which may connect many collections

# singelton client
client = MongoClient(MONGO_DB_HOST, MONGO_DB_PORT)

# default params
def get_db(db=DB_NAME):
  db = client[db]
  return db

