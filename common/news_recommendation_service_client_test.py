import news_recommendation_service_client as client

def test_basic():
  preference = client.getPreferenceForUser("user1")
  print(preference)
  assert preference is not None
  assert len(preference) > 0
  assert preference[0] == "World"
  print('test_basic passed!')

if __name__ == "__main__":
	test_basic()
