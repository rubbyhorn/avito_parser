import requests


HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:12.0) Gecko/20100101 Firefox/12.0",
    "Accept-Language": "en-US",
    "Accept-Encoding": "gzip, deflate",
    "Accept": "text/html",
    "Referer": "http://www.google.com/",
}


def get_page(url: str, query: str) -> str:
    response = requests.get(url.format(query),
                            headers=HEADERS)
    if response.status_code != requests.codes.OK:
        raise requests.exceptions.RequestException
    response.encoding = 'utf-8'
    return response.text
