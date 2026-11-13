import datetime
import time
import requests
import schedule
from bs4 import BeautifulSoup
n = 0
def get_book_data(book_url: str) -> dict:
    result = {}
    r = requests.request(url=book_url, method='get')
    for l in r.text.split('\n'):
        if l.strip().startswith('<th>'):
            info = l.strip()[4:-5].split('</th><td>')
            if len(info) == 2:
                result[info[0]] = info[1]
    return result
def scrape_books(is_save: bool, n=50):
    result = []
    for i in range(1, n + 1):
        url = 'http://books.toscrape.com/catalogue/page-' + str(i) + '.html'
        print(url)
        r = requests.request(url=url, method='get')
        for l in r.text.split('\n'):
            if l.strip().startswith('<h3><a href=') and 'title' in l:
                s = l.strip()[13:]
                u = 'http://books.toscrape.com/catalogue/' + s[:s.find('/')] + '/index.html'
                result.append(get_book_data(u))
    return result
def test_get_book_data():
    book_url = 'http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html'
    res = get_book_data(book_url)
    assert isinstance(res, dict) and len(res) >= 5
def test_scrape_books():
    res = scrape_books(is_save=False, n=1)
    assert isinstance(res, list) and len(res) >= 20
def do():
    global n
    n += 1
def test_schedule():
    schedule.every().second.do(do)
    ctime = datetime.datetime.now()
    while True:
        schedule.run_pending()
        time.sleep(1)
        if datetime.datetime.now() - ctime > datetime.timedelta(minutes=1):
            break
    assert n
test_get_book_data()
test_scrape_books()
test_schedule()

