! pip install -q schedule pytest   # установка библиотек, если ещё не
# Библиотеки, которые могут вам понадобиться
# При необходимости расширяйте список
import time
import requests
import schedule
from bs4 import BeautifulSoup
def get_book_data(book_url: str) -> dict:
    """
    Эта функция будет получать данные о книге с одной страницы.
    Входные параметры:
    book_url: str - адрес книги
    Результаты:
    result: dict - информация о книге
    """

    # НАЧАЛО ВАШЕГО РЕШЕНИЯ
    a, d, n, r, result = 0, 0, 0, ['', 'One', 'Two', 'Three', 'Four', 'Five'], {}
    request = requests.request(url=book_url, method='get')
    for l in request.text.split('\n'):
        if ' | ' in l: result['Name'] = l[4:l.find(' | ')]
        if a:
            result['Availability'] = int(l.strip()[14:-16]); a = 0
        if d and 'p' in l:
            result['Description'] = l.strip()[3:-8]; d = 0
        if n:
            result['Number of reviews'] = int(l.strip()[4:-5]); n = 0
        if 'Availability' in l: a = 1
        if 'Description' in l: d = 1
        if 'Number of reviews' in l: n = 1
        if 'star-rating' in l.strip():
            result['Rating'] = r.index(l.split()[2][:-2])
        if l.strip().startswith('<th>'):
            info = l.strip()[4:-5].split('</th><td>')
            if len(info) == 2:
                result[info[0]] = info[1].strip('Â£')
                if info[0].startswith('Price') or info[0] == 'Tax':
                    result[info[0]] = float(result[info[0]])
    return result
    # КОНЕЦ ВАШЕГО РЕШЕНИЯ
# Используйте для самопроверки
book_url = 'http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html'
get_book_data(book_url)
def scrape_books(is_save: bool, n=50):
    """
    Эта функция будет проходиться по всем страницам из каталога и осуществлять парсинг всех страниц в цикле, используя ранее написанную get_book_data.
    Входные параметры:
    is_save: bool - аргумент-флаг, который будет отвечать за сохранение результата в файл
    n: int - количество страниц, которые надо просмотреть
    Результаты:
    result: dict - информация о книгах
    """

    # НАЧАЛО ВАШЕГО РЕШЕНИЯ
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
    if is_save:
        with open('books_data.txt', 'w') as f:
            for l in result:
                f.write(str(l) + '\n')
    else:
        print(result)
    return result
    # КОНЕЦ ВАШЕГО РЕШЕНИЯ
# Проверка работоспособности функции
res = scrape_books(is_save=True)   # Допишите ваши аргументы
print(type(res), len(res), res)   # и проверки
# НАЧАЛО ВАШЕГО РЕШЕНИЯ
import schedule
import time
from datetime import datetime

def scrape():
    scrape_books(is_save=False, n=1)
print(datetime.now())
schedule.every().day.at('19:20').do(scrape)
while True:
    schedule.run_pending()
    time.sleep(1)
# Ячейка для демонстрации работоспособности
# Сам код напишите в отдельном скрипте
! pytest test/test_scraper.py
