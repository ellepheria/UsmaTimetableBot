import telebot

import config
import utils
from db import add_user, update_group, delete_user, get_user, get_group


bot = telebot.TeleBot(config.API_KEY)


@bot.message_handler(commands=['start'])
def get_text_messages(message):
    if not get_user(message.from_user.id):
        add_user(message.from_user)

    bot.send_message(message.from_user.id,
                     utils.generate_message(message.from_user.first_name, utils.get_timetable('ЛД 101', 1))
                     )


bot.polling(non_stop=True, interval=1)
