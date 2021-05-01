import requests
import traceback
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import sqlite3
import telebot
from threading import Thread
from entity import Entity
from config import parse_config
from downloader import get_page

DEBUG = True


def get_new_data():
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
                except BaseException:
                    print("Ошибка при загрузке.")
                    if DEBUG:
                        traceback.print_exc()
    except KeyError as e:
        print('Ашибка в конфиге. Неизвестный ключ {}.'.format(e))


def main():
    get_new_data()


if __name__ == '__main__':
    main()
else:
    main()
