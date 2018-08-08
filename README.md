# New-Scraping-and-Recommendation-System

## news_pipeline
a data pipeline which monitors, scrapes and dedupes latest news
(MongoDB, Redis, RabbitMQ, TF-IDF)

## web_server
a single-page web application for users to browse news 
(React, Node.js, RPC, SOA)

## news_recommendation_service
a click event log processor which collects users’ click logs, then updates a news preference model for each user 
(NLP)

## news_topic_modeling_service
an offline training pipeline for news topic modeling
(Tensorflow, CNN, NLP)
an online classifying service for news topic modeling using the trained model
