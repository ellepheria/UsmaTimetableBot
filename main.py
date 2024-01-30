import telebot

import config
from db import add_user, update_group, delete_user, get_user, get_group


bot = telebot.TeleBot(config.API_KEY)


@bot.message_handler(commands=['start'])
def get_text_messages(message):
    if not get_user(message.from_user.id):
        add_user(message.from_user)
    user = get_user(message.from_user.id)
    if get_group(message.from_user.id):
        bot.send_message(message.from_user.id, "Пользователь есть в системе, группа указана")
    else:
        bot.send_message(message.from_user.id, "Пользователь есть в системе, группа не указана")


bot.polling(non_stop=True, interval=1)
