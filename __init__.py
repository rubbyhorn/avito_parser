from telegram import init_bot
import db
from config import parse_config
from entity import get_new_data
import sys


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == "init":
        dates = get_new_data(parse_config())
        for data in dates:
            news = db.update_entities(data)
    init_bot()
