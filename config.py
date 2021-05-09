import json


def parse_config(file: str = 'config.json') -> dict:
    try:
        with open(file, 'rt') as config:
            try:
                config = json.load(config)
            except json.JSONDecodeError as e:
                print("Ашибка в конфиге. Строка:{str} Столбец:{col}"
                      "\nhttps://ru.wikipedia.org/wiki/JSON"
                      .format(str=e.lineno, col=e.colno))
                exit()
            except KeyError:
                print('Ашибка в конфиге. Не найден раздел "sites"')
                exit()
    except FileNotFoundError:
        print('Конфиг не найден. config.json должен находиться в той-же папке, что и db.py')
        exit()
    return config
