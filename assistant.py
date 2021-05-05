import os
import logging

import requests
from telegram import Update, ForceReply
from telegram.ext import (
    Updater, CommandHandler, MessageHandler,
    Filters, CallbackContext
)
from dotenv import load_dotenv
import re

load_dotenv()

TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
url_wttr = 'https://wttr.in/yaroslavl?format=j1&lang=ru'

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)


def start_command(update: Update, _: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def help_command(update: Update, _: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def parser_message(bot, update):
    message = bot.message.text
    if re.search(r'^[Ww]$', message):
        bot.message.reply_text(get_weather())
    else:
        bot.message.reply_text('?????')

def get_weather():
    try:
        response = requests.get(url_wttr)
        weather = response.json()
        with open('weatherTXT.json', 'w') as file:
            file.write(response.text)
        return 'Ok'
    except requests.exceptions.RequestException:
        logger.error('Error: get_weather')
        return 'Error get_weather'
    # print(mess)
    # bot.message.reply_text('parser_message Привет, я бот')
# response = requests.get(url)
# print(response.url)  # выдаст url запроса который был отправлен
# print(response.text)
    
    
def main():
    updater = Updater(TELEGRAM_TOKEN)
    dispatcher = updater.dispatcher
    
    dispatcher.add_handler(CommandHandler("start", start_command))
    dispatcher.add_handler(CommandHandler("help", help_command))

    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, parser_message))
    
    updater.start_polling()  # default 10.0sec (poll_interval=10.0)
    updater.idle()


if __name__ == '__main__':
    main()

# ============================================================================
# https://github.com/python-telegram-bot/python-telegram-bot/blob/master/examples/conversationbot2.py
'''
Одноразовые коды восстановления для heroku.com
HWC9E0M1MA
CDH35ZDSQ4
XY9R2WHT2V
0WYBKICFXQ
0M3SNKNQM3
42YQKVJBK6
JADL58VKLJ
S52KT1KOR0
RUDPW6Y28U
CL8VAD2HGV


'''