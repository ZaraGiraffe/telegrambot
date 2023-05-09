import telebot
import os
import shutil
from telebot.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

def token():
    return "5103709864:AAF1XqfUBGIKAzmT0IEeQOMBSg7Ic6FFDjU"

bot = telebot.TeleBot(token())


@bot.message_handler(commands=["createdeck"])
def create_deck(message):
    bot.send_message(message.chat.id, "type the name of the deck")
    bot.register_next_step_handler(message, create_deck2)


def create_deck2(message):
    if not "decks" in os.listdir("/"):
        os.mkdir("decks")
    try:
        os.mkdir(f"decks/{message.text}")
        bot.send_message(message.chat.id, f"created a deck")
    except:
        bot.send_message(message.chat.id, "something went wrong")


def abstract_choose_deck(message, next_func):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    for deck in os.listdir("decks"):
        markup.add(KeyboardButton(deck))
    markup.add(KeyboardButton("cancel"))
    bot.send_message(message.chat.id, "Choose deck", reply_markup=markup)
    bot.register_next_step_handler(message, next_func)


@bot.message_handler(commands=["deletedeck"])
def delete_deck(message):
    abstract_choose_deck(message, delete_deck2)


def delete_deck2(message):
    try:
        if message.text == "cancel":
            bot.send_message(message.chat.id, "ok", reply_markup=ReplyKeyboardRemove())
        else:
            shutil.rmtree(f"decks/{message.text}")
            bot.send_message(message.chat.id, "deleted a deck", reply_markup=ReplyKeyboardRemove())
    except:
        bot.send_message(message.chat.id, "something went wrong", reply_markup=ReplyKeyboardRemove())


@bot.message_handler(commands=["addimage"])
def add_image(message):
    abstract_choose_deck(message, add_image2)


def add_image2(message):
    deck = message.text
    bot.send_message(message.chat.id, "send image", reply_markup=ReplyKeyboardRemove())
    bot.register_next_step_handler(message, add_image3, deck)


def add_image3(message, deck):
    if message.content_type == "photo":
        imageID = message.photo[-1].file_id
        image_info = bot.get_file(imageID)
        image_file = bot.download_file(image_info.file_path)
        bot.send_message(message.chat.id, "choose name")
        bot.register_next_step_handler(message, add_image4, deck, image_file)
    else:
        bot.send_message(message.chat.id, "wrong type")


def add_image4(message, deck, image_file):
    name = message.text
    try:
        with open(f"decks/{deck}/{name}.jpg", "wb") as f:
            f.write(image_file)
        bot.send_message(message.chat.id, "added an image")
    except:
        bot.send_message(message.chat.id, "something went wrong")


bot.infinity_polling()