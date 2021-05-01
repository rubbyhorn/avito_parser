from typing import List
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from entity import Entity
from telebot import TeleBot

TOKEN = "1645136824:AAFbODOjntDM7m-I6NLvdO2JPmwY5TGkNiQ"
CHATID = "492438832"


def send_message(bot: TeleBot, chat_id: str, entity: Entity):
    markup = InlineKeyboardMarkup(row_width=1)
    button = InlineKeyboardButton(text="Перейти", url=entity.url)
    markup.add(button)
    bot.send_message(chat_id=chat_id,
                     text="📄 {title}\n📍 {geo}\n⌛ {lifeTime}\n {price} {priceCurrency}[⁣]({imgUrl})"
                     .format(title=entity.title,
                             geo=entity.geo,
                             lifeTime=entity.geo,
                             price=entity.price,
                             priceCurrency=entity.priceCurrency,
                             imgUrl=entity.imgUrl),
                     reply_markup=markup)


def send_messages(entities: List[Entity]):
    bot = TeleBot(TOKEN, parse_mode="markdown")

    for entity in entities:
        send_message(bot, chat_id=CHATID, entity=entity)

    # bot.polling()
