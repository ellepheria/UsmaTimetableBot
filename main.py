import telebot

import config
import utils
import constants
from db import add_user, update_group, delete_user, get_user, get_group


bot = telebot.TeleBot(config.API_KEY)


def ask_group(tg_id):
    bot.send_message(
        tg_id,
        'Укажите Вашу группу (например, ЛД 101)'
    )
    return


def ask_day(tg_id):
    bot.send_message(
        tg_id,
        'Укажите необходимый день недели (например, ПН)'
    )
    return


@bot.message_handler(commands=['start'])
def get_text_messages(message):
    if add_user(message.from_user):
        ask_group(message.from_user.id)
        return
    group = get_group(message.from_user.id)
    if not group:
        ask_group(message.from_user.id)
        return
    ask_day(message.from_user.id)
    return


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == constants.COMMANDS['GROUP_CHANGE']:
        ask_group(message.from_user.id)
        return
    if message.text in constants.GROUPS:
        update_group(message.from_user.id, message.text)
        ask_day(message.from_user.id)
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
