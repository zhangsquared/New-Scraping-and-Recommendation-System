""" Recommendation Service """

import operator  #pylint: disable=import-error, wrong-import-position
import logging
import os
import sys
# https://pypi.org/project/jsonrpclib-pelix/
from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
import mongodb_client #pylint: disable=import-error, wrong-import-position

PREFERENCE_TABLE_NAME= "user_preference_model"
SERVER_HOST = 'localhost'
SERVER_PORT = 5050

LOGGER_FORMAT = '%(asctime)s - %(message)s'
logging.basicConfig(format = LOGGER_FORMAT)
LOGGER = logging.getLogger('backend_server')
LOGGER.setLevel(logging.DEBUG)

# https://www.python.org/dev/peps/pep-0485/
def isclose(a, b, rel_tol=1e-9, abs_tol=0.0):
  return abs(a-b) <= max( rel_tol * max(abs(a), abs(b)), abs_tol )

def getPreferenceForUser(user_id):
  """Get user preference in an ordered class list."""
  print("query preference for " + user_id)
  db = mongodb_client.get_db()
  model = db[PREFERENCE_TABLE_NAME].find_one({ 'userId': user_id })

  if model is None:
    return []
  
  storted_tuples = sorted(list(model['preference'].items()), key=operator.itemgetter(1), reverse=True)
  sorted_list = [x[0] for x in storted_tuples]
  sorted_val_list = [x[1] for x in storted_tuples]

  # if the first preference is same as the ast one
  # the preference won't make any sense
  if isclose(float(sorted_val_list[0]), float(sorted_val_list[1])):
    return []
  
  return sorted_list

RPC_SERVER = SimpleJSONRPCServer((SERVER_HOST, SERVER_PORT))
RPC_SERVER.register_function(getPreferenceForUser, 'getPreferenceForUser')

LOGGER.info("Starting RPC server on %s:%d", SERVER_HOST, SERVER_PORT)

RPC_SERVER.serve_forever()
