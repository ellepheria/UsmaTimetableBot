import telebot

import config
import db


bot = telebot.TeleBot(config.API_KEY)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    db.add_user(message.from_user)
    if message.text == "Привет":
        bot.send_message(message.from_user.id, "Привет, чем я могу тебе помочь?")
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Напиши привет")
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")


bot.polling(non_stop=True, interval=0)
