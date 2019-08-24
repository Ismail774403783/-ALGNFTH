from datetime import datetime
import dateparser
import requests
from bs4 import BeautifulSoup
from bs4.element import Tag

BASE_URL = 'https://monocler.ru'
ARTICLES_URL = '%s/%s' % (BASE_URL, 'category/article')


class CantOpenError(BaseException):
    pass


def get_last_articles():
    response = requests.get(ARTICLES_URL)

    if response.status_code != 200:
        raise CantOpenError("Get wrong response status for URL %s!" % ARTICLES_URL)

    soup = BeautifulSoup(response.text, 'html.parser')
    articles_part = soup.findAll("div", {"id": "left-area"})

    articles = (article for article in articles_part[0].children if type(article) == Tag)
    year = datetime.now().year

    for article in articles:

        try:
            day, month, header, text, _ = tuple(article.stripped_strings)
            url = article.div.a.attrs['href']
            date = dateparser.parse('%s %s %s' % (day, month, year))
            print("%s, %s (%s)" % (date.strftime('%d.%m.%Y'), header, url))
            yield "%s, %s (%s)" % (date.strftime('%d.%m.%Y'), header, url)

        except ValueError:
            # TODO prettify this for last element which leads to next article page
            pass
