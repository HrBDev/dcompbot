# coding: utf-8
import logging
import os
import time

import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

import db

token = os.getenv('TOKEN')
bot = telebot.TeleBot(token)

logger = telebot.logger
telebot.logger.setLevel(logging.WARNING)  # Outputs debug messages to console.


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    chat_id = message.chat.id
    bot.send_chat_action(chat_id, 'typing')
    time.sleep(0.5)
    markup = InlineKeyboardMarkup()
    sections = db.get_sections()
    i = 0
    btn = []
    limit = int(len(sections) / 2)
    for section in sections:
        if i != 2:
            btn.append(InlineKeyboardButton(text=section[1], callback_data="option" +
                                                                           "-" + str(section[0])))
            i += 1
        if i == 2:
            markup.add(btn[0], btn[1])
            limit -= 1
            i = 0
            btn = []
        elif limit == 0:
            markup.add(InlineKeyboardButton(text=section[1], callback_data="option" +
                                                                           "-" + str(section[0])))
    bot.send_message(message.chat.id, "مقطع خود را انتخاب کنید؟", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.split("-")[0] == "section")
def send_field(call):
    chat_id = call.message.chat.id
    bot.send_chat_action(chat_id, 'typing')
    time.sleep(0.5)
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except Exception:
        pass
    markup = InlineKeyboardMarkup()
    sections = db.get_sections()
    i = 0
    btn = []
    limit = int(len(sections) / 2)
    for section in sections:
        if i != 2:
            btn.append(InlineKeyboardButton(section[1], callback_data="option" +
                                                                      "-" + str(section[0])))
            i += 1
        if i == 2:
            markup.add(btn[0], btn[1])
            limit -= 1
            i = 0
            btn = []
        elif limit == 0:
            markup.add(InlineKeyboardButton(section[1], callback_data="option" +
                                                                      "-" + str(section[0])))
    bot.send_message(call.message.chat.id, "در چه زمینه ای سوال دارید؟", reply_markup=markup)


@bot.callback_query_handler(
    func=lambda call: call.data.split("-")[0] == "option")
def show_options(call):
    chat_id = call.message.chat.id
    bot.send_chat_action(chat_id, 'typing')
    time.sleep(0.5)
    try:
        bot.delete_message(chat_id, call.message.message_id)
    except Exception:
        pass
    markup = InlineKeyboardMarkup()
    options = db.get_options(id_section=call.data.split("-")[1])
    i = 0
    btn = []
    limit = int(len(options) / 2)
    for option in options:
        if i != 2:
            btn.append(InlineKeyboardButton(text=option[2],
                                            callback_data="content" +
                                                          "-" + str(option[0]) +
                                                          "-" + str(call.data.split("-")[1])))
            i += 1
        if i == 2:
            markup.add(btn[0], btn[1])
            limit -= 1
            i = 0
            btn = []
        elif limit == 0:
            markup.add(InlineKeyboardButton(text=option[2],
                                            callback_data="content" +
                                                          "-" + str(option[0]) +
                                                          "-" + str(call.data.split("-")[1])))
    markup.add(InlineKeyboardButton("بازگشت", callback_data="section"))
    bot.send_message(call.message.chat.id, "در چه زمینه ای سوال دارید؟", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.split("-")[0] == "content")
def show_contents(call):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    bot.send_chat_action(chat_id, 'typing')
    time.sleep(0.5)
    try:
        bot.delete_message(chat_id, message_id)
    except Exception:
        pass
    markup = InlineKeyboardMarkup()
    contents = db.get_content(id_option=call.data.split("-")[1])
    i = 0
    btn = []
    limit = int(len(contents) / 2)
    for content in contents:
        if i != 2:
            btn.append(InlineKeyboardButton(text=content[2],
                                            callback_data="content_fill" +
                                                          "-" + str(content[0])))
            i += 1
        if i == 2:
            markup.add(btn[0], btn[1])
            limit -= 1
            i = 0
            btn = []
        elif limit == 0:
            markup.add(InlineKeyboardButton(text=content[2],
                                            callback_data="content_fill" +
                                                          "-" + str(content[0])))
    markup.add(InlineKeyboardButton("بازگشت", callback_data="option" +
                                                            "-" + str(call.data.split("-")[2])))
    bot.send_message(call.message.chat.id,
                     db.get_path_content(call.data.split("-")[1]) + " ," "در چه زمینه ای سوال دارید؟",
                     reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.split("-")[0] == "content_fill")
def show_content_filled(call):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    try:
        bot.delete_message(chat_id, message_id)
    except Exception:
        pass
    results = db.get_content_filled(id_content=call.data.split("-")[1])
    for result in results:
        path = db.get_path_content_filled(call.data.split("-")[1])
        bot.send_message(chat_id, path)
        if result[0] == 1:
            bot.send_chat_action(chat_id, 'typing')
            time.sleep(1)
            bot.send_message(chat_id, text=result[1])
        elif result[0] == 2:
            bot.send_chat_action(chat_id, 'upload_document')
            time.sleep(1)
            try:
                file = open(result[1], 'rb')
                ext = result[1].split(".")[1]
                if ext in ["png", "jpeg", "jpg", "PNG", "JPEG", "JPG"]:
                    bot.send_photo(chat_id, file)
                else:
                    bot.send_document(chat_id, file)
            except IOError:
                pass
    send_welcome(call.message)


bot.polling(none_stop=True, interval=0, timeout=20)
