#!/bin/bash
service redis_6379 start
service mongod start

pip3 install -r requirements.txt

# Launch news topic modeling server
cd news_topic_modeling_service
cd server
python3 server.py &

# Launch news data scrapping pipeline
cd ../../news_pipeline
python3 news_monitor.py &
python3 news_fetcher.py &
python3 news_deduper.py &

echo "=================================================="
read -p "PRESS [ENTER] TO TERMINATE PROCESSES." PRESSKEY

kill $(jobs -p)
 