""" Backend service """

# pip3 freeze > requirements.txt
import operations  #pylint: disable=import-error, wrong-import-position
import logging
# https://pypi.org/project/jsonrpclib-pelix/
from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer

SERVER_HOST = 'localhost'
SERVER_PORT = 4040

LOGGER_FORMAT = '%(asctime)s - %(message)s'
logging.basicConfig(format = LOGGER_FORMAT)
LOGGER = logging.getLogger('backend_server')
LOGGER.setLevel(logging.DEBUG)

def add(num1, num2):
    """ Test """
    # python docstring
    LOGGER.debug('add is callled with %d and %d', num1, num2)
    return num1 + num2


def get_one_news():
    """ Test method to get one news """
    LOGGER.debug("getOneNews is called")
    return operations.getOneNews()

def get_news_summaries_for_user(user_id, page_num):
    """get news summaries for a user"""
    LOGGER.debug("get_news_summaries_for_user is called with %s and %s", user_id, page_num)
    return operations.getNewsSummariesForUser(user_id, page_num)

def log_news_click_for_user(user_id, news_id):
    """log a news click event for a user."""
    LOGGER.debug("log_news_click_for_user is called with %s and %s", user_id, news_id)
    return operations.logNewsClickForUser(user_id, news_id)

RPC_SERVER = SimpleJSONRPCServer((SERVER_HOST, SERVER_PORT))
RPC_SERVER.register_function(add, 'add')
RPC_SERVER.register_function(get_one_news, 'getOneNews')
RPC_SERVER.register_function(get_news_summaries_for_user, 'getNewsSummariesForUser')
RPC_SERVER.register_function(log_news_click_for_user, 'logNewsClickForUser')

LOGGER.info("Starting RPC server on %s:%d", SERVER_HOST, SERVER_PORT)

RPC_SERVER.serve_forever()

