import news_fetcher
import time

INTERNVAL = 30

def test_parser():
  url = 'http://www.bloomberg.com/news/articles/2018-07-09/canada-s-30-billion-lng-hope-edges-closer-as-shell-ramps-up'
  url2 = 'http://www.bloomberg.com/news/articles/2018-07-09/face-of-brexit-boris-johnson-resigns-plunging-may-into-crisis'
  url3 = 'http://www.bloomberg.com/news/articles/2018-07-09/erdogan-hands-economy-job-to-son-in-law-as-old-a-team-bows-out'

  t = news_fetcher.fetch(url)
  print(t)
  assert len(t) > 0

  time.sleep(INTERNVAL)
  
  t = news_fetcher.fetch(url3)
  print(t)
  assert len(t) > 0

  time.sleep(INTERNVAL)

  t = news_fetcher.fetch(url2)
  print(t)
  assert len(t) > 0

  print("pass test_parser")

def test_handle_message():
  news_fetcher.handle_message(None)
  # news_fetcher.handle_message()


if __name__ == '__main__':
  test_parser()