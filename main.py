import telebot

import config
import utils
import constants
from db import add_user, update_group, delete_user, get_user, get_group


bot = telebot.TeleBot(config.API_KEY)


def send_timetable_by_day():
    pass


def group_handler():
    pass


@bot.message_handler(commands=['start'])
def get_text_messages(message):
    if add_user(message.from_user):
        bot.send_message(
            message.from_user.id,
            'Укажите Вашу группу (например, ЛД 101)'
        )
        return
    group = get_group(message.from_user.id)
    if not group:
        bot.send_message(
            message.from_user.id,
            'Укажите Вашу группу (например, ЛД 101)'
        )
        return
    bot.send_message(
        message.from_user.id,
        'Укажите необходимый день недели (например, ПН)'
    )
    return


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text in constants.GROUPS:
        update_group(message.from_user.id, message.text)
        bot.send_message(
            message.from_user.id,
            'Укажите необходимый день недели (например, ПН)'
        )
        return
    if message.text in constants.DAY_TO_DATE:
        group = get_group(message.from_user.id)
        date = constants.DAY_TO_DATE[message.text]
        bot.send_message(
            message.from_user.id,
            utils.generate_message(message.from_user.first_name, utils.get_timetable(group, date))
        )
        return
    bot.send_message(
        message.from_user.id,
        'Я Вас не понимаю, попробуйте еще раз'
    )
    return


bot.polling(non_stop=True, interval=1)
