from unittest.mock import MagicMock
import news_monitor as moniter

mock_news_api_client = MagicMock()

def test_basic():
    moniter.run(mock_news_api_client)
    print('test_basic passed!')

if __name__ == "__main__":
    test_basic()
