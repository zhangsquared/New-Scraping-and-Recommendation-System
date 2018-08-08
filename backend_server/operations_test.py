import operations
import os
import sys

# import common package in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
from cloudAMQP_client import CloudAMQPClient #pylint: disable=import-error, wrong-import-position
CLICK_QUEUE_URL = ""
ClICK_QUEUE_NAME = "news-click-queue"
click_client = CloudAMQPClient(CLICK_QUEUE_URL, ClICK_QUEUE_NAME)

userName = 'test'

def test_getOneNews_basic():
    news = operations.getOneNews()
    # print(news)
    assert news is not None
    print('test_getOneNews_basic passed!')

def test_getNewsSummariesForUser_basic():
    news = operations.getNewsSummariesForUser(userName, 1)
    assert len(news) > 0
    print('test_getNewsSummariesForUser_basic passed!')

def test_getNewsSummariesForUser_invalid_pageNum():
    news = operations.getNewsSummariesForUser(userName, -1)
    assert len(news) == 0
    print('test_getNewsSummariesForUser_invalid_pageNum passed!')

def test_getNewsSummariesForUser_large_pageNum():
    news = operations.getNewsSummariesForUser(userName, 1000)
    assert len(news) == 0
    print('test_getNewsSummariesForUser_large_pageNum passed!')

def test_getNewsSummariesForUser_pagination():
    news1 = operations.getNewsSummariesForUser(userName, 1)
    news2 = operations.getNewsSummariesForUser(userName, 2)
    assert len(news1) > 0
    assert len(news2) > 0

    digest_page1 = set([news['digest'] for news in news1])
    digest_page2 = set([news['digest'] for news in news2])

    l = len(digest_page1.intersection(digest_page2))
    assert l == 0

    print('test_getNewsSummariesForUser_pagination passed!')

def test_logNewsClickForUser():
    operations.logNewsClickForUser(userName, "news1")
    click_client.sleep(3)
    msg = click_client.getMessage()
    assert msg['userId'] == userName
    assert msg['newsId'] == 'news1'

    print('test_logNewsClickForUser passed!')

def test_getNewsSummariesForUser_click():
    operations.logNewsClickForUser("user1", "news1")
    click_client.sleep(3)
    news = operations.getNewsSummariesForUser("user1", 1)
    for one_news in news:
        if one_news['class'] is not None:
            if one_news['class'] == 'World':
                assert one_news['reason'] == 'recommended'
            else:
                assert 'reason' not in one_news
    print('test_getNewsSummariesForUser_click passed!')


if __name__ == "__main__":
    # test_getOneNews_basic()
    # test_getNewsSummariesForUser_basic()
    # test_getNewsSummariesForUser_invalid_pageNum()
    # test_getNewsSummariesForUser_large_pageNum()
    # test_getNewsSummariesForUser_pagination()
    # test_logNewsClickForUser()
    test_getNewsSummariesForUser_click()

