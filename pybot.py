import telebot
import logging
import time
import db
from telebot import types

token = <Token>
bot = telebot.TeleBot(token)

logger = telebot.logger
telebot.logger.setLevel(logging.WARNING)  # Outputs debug messages to console.


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    chat_id = message.chat.id
    time.sleep(1)
    bot.send_chat_action(chat_id, 'typing')
    markup = types.InlineKeyboardMarkup()
    options = db.get_sections()
    i = 0
    btn = []
    limit = int(len(options) / 2)
    for option in options:
        if i != 2:
            btn.append(types.InlineKeyboardButton(text=option[1], callback_data=str(option[0]) + "-" + option[1]))
            db.get_id(str(option[0]), option[1])
            i += 1
        if i == 2:
            markup.add(btn[0], btn[1])
            limit -= 1
            i = 0
            btn = []
        elif limit == 0:
            markup.add(types.InlineKeyboardButton(text=option[1], callback_data=str(option[0]) + "-" + option[1]))
    bot.send_message(message.chat.id, "مقطع خود را انتخاب کنید؟", reply_markup=markup)


@bot.callback_query_handler(
    func=lambda call: len(call.data.split("-")) == 4 and db.get_id_content(call.data.split("-")[1],
                                                                           call.data.split("-")[2],
                                                                           call.data.split("-")[3]))
def show_content_filled(call):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    # action_string can be one of the following strings: 'typing', 'upload_photo', 'record_video', 'upload_video',
    # 'record_audio', 'upload_audio', 'upload_document' or 'find_location'.
    # bot.send_chat_action(chat_id, 'typing')
    # time.sleep(1.5)
    try:
        bot.delete_message(chat_id, message_id)
    except Exception:
        pass
    texts = db.get_content_filled(call.data.split("-")[1])
    bot.send_chat_action(chat_id, 'typing')
    texts2 = db.get_content_filled_msg(call.data.split("-")[1])
    bot.send_message(call.message.chat.id, text=texts2)

    for text in texts:
        if text[5] is 2:
            bot.send_chat_action(chat_id, 'upload_document')
            time.sleep(0.5)
            file = open(text[2], 'rb')
            temp = text[2].split("/")
            if temp[len(temp) - 1].split(".")[1] in ["png", "jpeg", "jpg", "PNG", "JPEG", "JPG"]:
                bot.send_photo(chat_id, file)
            else:
                bot.send_document(chat_id, file)
        elif text[5] is 1:
            bot.send_chat_action(chat_id, 'typing')
            time.sleep(1)
            bot.send_message(call.message.chat.id, text=text[2])
    send_welcome(call.message)


@bot.callback_query_handler(
    func=lambda call: len(call.data.split("-")) == 3 and db.get_id_option(call.data.split("-")[0],
                                                                          call.data.split("-")[1],
                                                                          call.data.split("-")[2]))
def show_contents(call):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    bot.send_chat_action(chat_id, 'typing')
    time.sleep(0.5)
    try:
        bot.delete_message(chat_id, message_id)
    except Exception:
        pass
    markup = types.InlineKeyboardMarkup()
    contents = db.get_content(call.data.split("-")[0])
    i = 0
    btn = []
    limit = int(len(contents) / 2)
    for content in contents:
        if i != 2:
            print("1-" + str(content[0]) + "-" + str(content[1]) + "-" +
                  content[
                      2])
            btn.append(types.InlineKeyboardButton(content[2],
                                                  callback_data="1-" + str(content[0]) + "-" + str(content[1]) + "-" +
                                                                content[
                                                                    2]))
            i += 1
        if i == 2:
            markup.add(btn[0], btn[1])
            limit -= 1
            i = 0
            btn = []
        elif limit == 0:
            markup.add(types.InlineKeyboardButton(content[2],
                                                  callback_data="1-" + str(content[0]) + "-" + str(content[1]) + "-" +
                                                                content[
                                                                    2]))
    markup.add(
        types.InlineKeyboardButton("بازگشت", callback_data=call.data.split("-")[1] + "-" + call.data.split("-")[2]))
    texts2 = db.get_content_msg(call.data.split("-")[0])
    texts2 += " ، در چه زمینه ای سوال دارید؟"
    bot.send_message(call.message.chat.id, texts2, reply_markup=markup)


@bot.callback_query_handler(
    func=lambda call: len(call.data.split("-")) == 2 and db.get_id(call.data.split("-")[0], call.data.split("-")[1]))
def show_options(call):
    chat_id = call.message.chat.id
    bot.send_chat_action(chat_id, 'typing')
    time.sleep(0.5)
    try:
        bot.delete_message(chat_id, call.message.message_id)
    except Exception:
        pass
    markup = types.InlineKeyboardMarkup()
    options = db.get_options(call.data.split("-")[0])
    i = 0
    btn = []
    limit = int(len(options) / 2)
    for option in options:
        if i != 2:
            btn.append(types.InlineKeyboardButton(option[2],
                                                  callback_data=str(option[0]) + "-" + str(option[1]) + "-" + option[
                                                      2]))
            i += 1
        if i == 2:
            markup.add(btn[0], btn[1])
            limit -= 1
            i = 0
            btn = []
        elif limit == 0:
            markup.add(types.InlineKeyboardButton(option[2],
                                                  callback_data=str(option[0]) + "-" + str(option[1]) + "-" + option[
                                                      2]))
    markup.add(
        types.InlineKeyboardButton("بازگشت", callback_data=call.data.split("-")[0]))
    bot.send_message(call.message.chat.id, "در چه زمینه ای سوال دارید؟", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: len(call.data) == 1 and db.get_id_section(call.data))
def send_field(call):
    chat_id = call.message.chat.id
    bot.send_chat_action(chat_id, 'typing')
    time.sleep(0.5)
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except Exception:
        pass
    markup = types.InlineKeyboardMarkup()
    options = db.get_sections()
    i = 0
    btn = []
    limit = int(len(options) / 2)
    for option in options:
        if i != 2:
            btn.append(types.InlineKeyboardButton(option[1], callback_data=str(option[0]) + "-" + option[1]))
            db.get_id(str(option[0]), option[1])
            i += 1
        if i == 2:
            markup.add(btn[0], btn[1])
            limit -= 1
            i = 0
            btn = []
        elif limit == 0:
            markup.add(types.InlineKeyboardButton(option[1], callback_data=str(option[0]) + "-" + option[1]))
    bot.send_message(call.message.chat.id, "در چه زمینه ای سوال دارید؟", reply_markup=markup)


try:
    bot.polling(none_stop=True)
except Exception as e:
    logger.error(e)
    time.sleep(20)
    pass
finally:
    db.cnx.close()
