# Message Queue:
# https://www.cloudamqp.com/docs/index.html
# Python lib:
# https://pika.readthedocs.io/en/0.10.0/
# https://www.rabbitmq.com/tutorials/tutorial-one-python.html

import logging
import json
import pika

LOGGER_FORMAT = '%(asctime)s - %(message)s'
logging.basicConfig(format = LOGGER_FORMAT)
LOGGER = logging.getLogger('backend_server')
LOGGER.setLevel(logging.DEBUG)

class CloudAMQPClient:

  def __init__(self, cloud_amqp_url, queue_name):
    self.cloud_amqp_url = cloud_amqp_url
    self.queue_name = queue_name
    self.params = pika.URLParameters(cloud_amqp_url)
    self.params.socket_timeout = 3 # only allow to retry to build connection for 3 seconds
    self.connection = pika.BlockingConnection(self.params)
    self.channel = self.connection.channel()
    self.channel.queue_declare(queue=queue_name)
  
  # Send a message
  def sendMessage(self, message):
    # json dumps is used to flatten JSON
    # message is json object, when send message to queue, need to convert it to string
    self.channel.basic_publish(exchange='', routing_key=self.queue_name, body=json.dumps(message))
    LOGGER.debug("[x] send message to %s: %s", self.queue_name, message)

  # Get a message. If not message, return None
  def getMessage(self):
    method_frame, header_frame, body = self.channel.basic_get(self.queue_name)
    # if error , method_frame null
    if method_frame:
      LOGGER.debug("[x] get message from %s: %s", self.queue_name, body)
      # send back to AMQP server to drop message 
      self.channel.basic_ack(method_frame.delivery_tag)
      # decode bytes to string, then convert tstring to json
      return json.loads(body.decode('utf-8'))
    else:
      LOGGER.debug("no message returned")
      return None

  # BlockingConnection.sleep is a safer way to sleep than time.sleep()
  # this will respond to cloudAMQP server's heartbeat
  def sleep(self, seconds):
    self.connection.sleep(seconds)