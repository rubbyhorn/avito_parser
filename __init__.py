import json
import requests
import traceback
from urllib.parse import urlparse, urlunparse

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


def main():
    sites = parse_config()
    try:
        for site in sites:
            for query in site["queries"]:
                try:
                    url = site["url"]
                    try:
                        page = get_page(url, query)
                    except requests.exceptions.RequestException as e:
                        print("Ашибка HTTP. Чет с сетью.\n{}".format(e))
                        raise e
                    filename = "_".join((urlparse(url).netloc.replace(".", "_"),
                                         query.replace(" ", "_"))) + '.html'

                    with open(filename, "wb")as file:
                        file.write(bytes(page, encoding='utf-8'))
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
