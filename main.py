import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

import config
import utils
import constants
from db import add_user, update_group, delete_user, get_user, get_group


bot = telebot.TeleBot(config.API_KEY)


def ask_group(tg_id):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.keyboard = [
        [constants.GROUPS[0], constants.GROUPS[1]],
        [constants.GROUPS[2], constants.GROUPS[3]],
    ]
    bot.send_message(
        tg_id,
        'Укажите Вашу группу (например, ЛД 101)',
        reply_markup=markup,
    )


def ask_day(tg_id):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.keyboard = [
        [constants.DAYS[0], constants.DAYS[1], constants.DAYS[2]],
        [constants.DAYS[3], constants.DAYS[4], constants.DAYS[5]],
        [constants.COMMANDS['GROUP_CHANGE']],
    ]
    bot.send_message(
        tg_id,
        'Укажите необходимый день недели (например, ПН)',
        reply_markup=markup
    )


def send_error_message(tg_id):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.keyboard = [
        ['/start']
    ]

    bot.send_message(
        tg_id,
        'Я Вас не понимаю, попробуйте начать сначала',
        reply_markup=markup
    )


def send_timetable(message):
    group = get_group(message.from_user.id)
    date = constants.DAY_TO_DATE[message.text]

    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.keyboard = [
        [constants.DAYS[0], constants.DAYS[1], constants.DAYS[2]],
        [constants.DAYS[3], constants.DAYS[4], constants.DAYS[5]],
        [constants.COMMANDS['GROUP_CHANGE']],
    ]

    bot.send_message(
        message.from_user.id,
        utils.generate_message(message.from_user.first_name, utils.get_timetable(group, date)),
        reply_markup=markup
    )


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
    if message.text in constants.DAYS:
        send_timetable(message)
        return
    send_error_message(message.from_user.id)


bot.polling(non_stop=True, interval=1)
