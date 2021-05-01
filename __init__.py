import asyncio
import json
import scrapy
import scrapy.crawler

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:12.0) Gecko/20100101 Firefox/12.0",
    "Accept-Language": "en-US",
    "Accept-Encoding": "gzip, deflate",
    "Accept": "text/html",
    "Referer": "http://www.google.com/",
}


class MySpider(scrapy.Spider):
    name = 'myspider'

    custom_settings = {
        'SOME_SETTING': 'some value',
    }

    def __init__(self, url, queries):
        self.url = url
        self.queries = queries

    def start_requests(self):
        return [scrapy.FormRequest(self.url.format(query), method="GET", headers=headers,
                                   callback=self.logged_in) for query in self.queries]

    def logged_in(self, response):
        with open(str(response.url)[-3:]+'html', 'wt') as file:
            file.write(str(response.body))


def parce_config(file='config.json'):
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
                print('Ашибка в конфиге. Не найден раздел "queries"')
                exit()
    except FileNotFoundError:
        print('Конфиг не найден. config.json должен находиться в той-же папке, что и __init__.py')
        exit()
    return config


async def main():
    config = parce_config()
    process = scrapy.crawler.CrawlerProcess()
    config = config[0]
    process.crawl(MySpider, config["url"], config["queries"])
    process.start()
    print("adas\n"*10)

if __name__ == '__main__':
    asyncio.run(main())
else:
    asyncio.run(main())
