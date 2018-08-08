import jsonrpclib

URL = 'http://localhost:5050'

client = jsonrpclib.ServerProxy(URL)

def getPreferenceForUser(user_id):
  preference = client.getPreferenceForUser(user_id)
  return preference
