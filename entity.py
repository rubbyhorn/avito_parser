import bs4.element
from urllib.parse import urljoin
from downloader import get_page
import requests
import traceback
from urllib.parse import urlparse
from bs4 import BeautifulSoup


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

    def get_tuple(self):
        return self.id, self.url, self.imgUrl, self.title, self.price, self.priceCurrency, self.lifeTime, self.geo

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


def get_new_data(config):
    result = []
    try:
        for query in config["queries"]:
            try:
                url = config["url"]
                domain = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(url))
                try:
                    page = get_page(url, query)
                except requests.exceptions.RequestException as e:
                    print("Ашибка HTTP. Чет с сетью.\n{}".format(e))
                    raise e
                soup = BeautifulSoup(page, "lxml")

                entities = map(lambda x: Entity(domain, x),
                               soup.select('div[data-marker="catalog-serp"] div[data-marker="item"]'))
                result.append(list(entities))
            except BaseException:
                print("Ошибка при загрузке.")
                traceback.print_exc()
    except KeyError as e:
        print('Ашибка в конфиге. Неизвестный ключ {}.'.format(e))

    return result
