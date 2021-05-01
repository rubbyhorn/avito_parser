import requests
import traceback
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import sqlite3
from telegram import send_messages
from threading import Thread
from entity import Entity
from config import parse_config
from downloader import get_page


DEBUG = True

# class TelegramThread(Thread):
#
#     def __init__(self):
#         """Инициализация потока"""
#         Thread.__init__(self)
#
#     def run(self):
#         get_new_data()




def get_new_data():
    sites = parse_config()
    result = []
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

                    entities = map(lambda x: Entity(domain, x),
                                  soup.select('div[data-marker="catalog-serp"] div[data-marker="item"]'))
                    filename = "_".join((urlparse(url).netloc.replace(".", "_"),
                                         query.replace(" ", "_"))) + '.html'
                    result.append(list(entities))
                    with open(filename, "wb")as file:
                        for entitie in entities:
                            file.write(bytes(str(result), encoding='utf-8'))
                except BaseException:
                    print("Ошибка при загрузке.")
                    if DEBUG:
                        traceback.print_exc()
    except KeyError as e:
        print('Ашибка в конфиге. Неизвестный ключ {}.'.format(e))

    return result


def main():

    send_messages(get_new_data()[0][:2])


if __name__ == '__main__':
    main()
else:
    main()
