from typing import List
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from entity import Entity
from telebot import TeleBot
import db
from config import parse_config
from entity import get_new_data

TOKEN = parse_config()['token']


def init_bot():
    bot = TeleBot(TOKEN, parse_mode="markdown")

    @bot.message_handler(commands=["update"])
    def update(message):
        chat_id = message.chat.id
        config = parse_config()
        dates = get_new_data(config)
        for data, query in zip(dates, config["queries"]):
            news = db.update_entities(data)  # list of news
            if len(news):
                send_messages(news, chat_id)
            else:
                bot.reply_to(message, query+": Ничего нового")

    bot.polling()


def send_message(bot: TeleBot, chat_id: str, entity: Entity):
    markup = InlineKeyboardMarkup(row_width=1)
    button = InlineKeyboardButton(text="Перейти", url=entity.url)
    markup.add(button)
    bot.send_message(chat_id,
                     text="{title}\n📍 {geo}\n⌛ {lifeTime}\n💲 {price} {priceCurrency}[⁣]({imgUrl})"
                     .format(title=entity.title,
                             geo=entity.geo,
                             lifeTime=entity.lifeTime,
                             price=entity.price,
                             priceCurrency=entity.priceCurrency,
                             imgUrl=entity.imgUrl),
                     reply_markup=markup)


def send_messages(entities: List[Entity], chat_id):
    bot = TeleBot(TOKEN, parse_mode="markdown")
    for entity in entities:
        send_message(bot, chat_id=chat_id, entity=entity)
