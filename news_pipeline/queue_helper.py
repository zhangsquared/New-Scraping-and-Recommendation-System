import os
import sys

# import common package in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

from cloudAMQP_client import CloudAMQPClient #pylint: disable=import-error, wrong-import-position

SCRAPER_QUEUE_URL = ""
SCRAPER_QUEUE_NAME = "news-scraper-queue"

DEDUPER_QUEUE_URL = ""
DEDUPER_QUEUE_NAME = "news-deduper-queue"

def clearQueue(url, name):
  queue_client = CloudAMQPClient(url, name)
  num_of_msg = 0

  while True:
    if queue_client is not None:
      msg = queue_client.getMessage()
      if msg is None:
        print("Cleared %d messages." %num_of_msg)
        return
      num_of_msg += 1

if __name__ == "__main__":
    clearQueue(SCRAPER_QUEUE_URL, SCRAPER_QUEUE_NAME)
    clearQueue(DEDUPER_QUEUE_URL, DEDUPER_QUEUE_NAME)
