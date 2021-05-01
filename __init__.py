import json
import requests
import traceback
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import bs4.element

DEBUG = True

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:12.0) Gecko/20100101 Firefox/12.0",
    "Accept-Language": "en-US",
    "Accept-Encoding": "gzip, deflate",
    "Accept": "text/html",
    "Referer": "http://www.google.com/",
}


def parse_config(file: str = 'config.json') -> list:
    config = {}
    try:
        with open(file, 'rt') as config:
            try:
                config = json.load(config)
                config = config["sites"]
            except json.JSONDecodeError as e:
                print("Ашибка в конфиге. Строка:{str} Столбец:{col}"
                      "\nhttps://ru.wikipedia.org/wiki/JSON"
                      .format(str=e.lineno, col=e.colno))
                exit()
            except KeyError:
                print('Ашибка в конфиге. Не найден раздел "sites"')
                exit()
    except FileNotFoundError:
        print('Конфиг не найден. config.json должен находиться в той-же папке, что и __init__.py')
        exit()
    return config


def get_page(url: str, query: str) -> str:
    response = requests.get(url.format(query),
                            headers=HEADERS)
    if response.status_code != requests.codes.OK:
        raise requests.exceptions.RequestException
    response.encoding = 'utf-8'
    return response.text


class Entity:
    def __init__(self, domain: str, tag: bs4.element.Tag):
        try:
            self.id = tag.get("id")
        except:
            self.id = None

        try:
            self.url = urljoin(domain, tag.select('a[itemprop="url"]').pop().get("href"))
        except:
            self.url = None

        try:
            self.imgUrl = tag.select('a[itemprop="url"] li')\
                .pop().get("data-marker").replace("slider-image/image-", "")
        except:
            self.imgUrl = None

        try:
            self.title = tag.select('a[itemprop="url"]')\
                .pop().get("title")
        except:
            self.title = None

        try:
            self.price = tag.select('span[data-marker="item-price"] meta[itemprop="price"]')\
                .pop().get("content")
        except:
            self.price = None

        try:
            self.priceCurrency = tag.select('span[data-marker="item-price"] meta[itemprop="priceCurrency"]')\
                .pop().get("content")
        except:
            self.priceCurrency = None

        try:
            self.lifeTime = tag.select('div[data-marker="item-date"]')\
                .pop().text
        except:
            self.lifeTime = None

        try:
            self.geo = tag.select('span[class^="geo"]')\
                .pop().text
        except:
            self.geo = None

    def __str__(self):
        return "id: {id}\n" \
               "url: {url}\n" \
               "imgUrl: {imgUrl}\n" \
               "title: {title}\n" \
               "price: {price}\n" \
               "lifeTime: {lifeTime}\n" \
               "geo: {geo}\n" \
               "\n".\
                format(id=self.id,
                       url=self.url,
                       imgUrl=self.imgUrl,
                       title=self.title,
                       price=self.price+" "+self.priceCurrency,
                       lifeTime=self.lifeTime,
                       geo=self.geo)


def main():
    sites = parse_config()
    try:
        for site in sites:
            for query in site["queries"]:
                try:
                    url = site["url"]
                    domain = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(url))
                    try:
                        page = get_page(url, query)
                    except requests.exceptions.RequestException as e:
                        print("Ашибка HTTP. Чет с сетью.\n{}".format(e))
                        raise e
                    soup = BeautifulSoup(page, "lxml")

                    results = map(lambda x: Entity(domain, x),
                                  soup.select('div[data-marker="catalog-serp"] div[data-marker="item"]'))
                    filename = "_".join((urlparse(url).netloc.replace(".", "_"),
                                         query.replace(" ", "_"))) + '.html'

                    with open(filename, "wb")as file:
                        for result in results:
                            file.write(bytes(str(result), encoding='utf-8'))
                except BaseException as e:
                    print("Ошибка при загрузке.")
                    if DEBUG:
                        traceback.print_exc()
    except KeyError as e:
        print('Ашибка в конфиге. Неизвестный ключ {}.'.format(e))


if __name__ == '__main__':
    main()
else:
    main()
