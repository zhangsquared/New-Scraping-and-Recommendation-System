#!/bin/bash
service redis_6379 start
service mongod start

pip install -r requirements.txt

# Launch UI Server
cd web_server
cd client
npm install
npm run build
cd ../server
npm install
npm start &

# Launch backend server
cd ../../backend_server
python3 service.py &

# Launch recommendation server
cd ../news_recommendation_service
python3 recommendation_service.py &

# Launch click processor
python3 click_log_processor.py &

echo "=================================================="
read -p "PRESS [ENTER] TO TERMINATE PROCESSES." PRESSKEY

kill $(jobs -p)
