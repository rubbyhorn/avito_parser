import bs4.element
from urllib.parse import urljoin


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
