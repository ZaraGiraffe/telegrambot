import telebot
import os
import shutil
from telebot.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
import json
from random import shuffle

def token():
    return "5103709864:AAF1XqfUBGIKAzmT0IEeQOMBSg7Ic6FFDjU"

bot = telebot.TeleBot(token())


@bot.message_handler(commands=["adddeck"])
def add_deck(message):
    bot.send_message(message.chat.id, "type the name of the deck")
    bot.register_next_step_handler(message, add_deck2)


def add_deck2(message):
    deck = message.text
    if not "decks" in os.listdir("./"):
        print(os.listdir("./"))
        os.mkdir("decks")
    try:
        os.mkdir(f"decks/{deck}")
        empty = []
        with open(f"decks/{deck}/statistics.json", "w") as f:
            f.write(json.dumps(empty))
        bot.send_message(message.chat.id, f"added a deck")
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
    deck = message.text
    try:
        if deck == "cancel":
            bot.send_message(message.chat.id, "ok", reply_markup=ReplyKeyboardRemove())
            return
        else:
            shutil.rmtree(f"decks/{deck}")
            bot.send_message(message.chat.id, "deleted a deck", reply_markup=ReplyKeyboardRemove())
    except:
        bot.send_message(message.chat.id, "something went wrong", reply_markup=ReplyKeyboardRemove())


@bot.message_handler(commands=["addimage"])
def add_image(message):
    abstract_choose_deck(message, add_image2)


def add_image2(message):
    deck = message.text
    if deck == "cancel":
        bot.send_message(message.chat.id, "ok", reply_markup=ReplyKeyboardRemove())
        return
    elif deck not in os.listdir("decks"):
        bot.send_message(message.chat.id, "there is no such deck", reply_markup=ReplyKeyboardRemove())
        return
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("cancel"))
    bot.send_message(message.chat.id, "send image", reply_markup=markup)
    bot.register_next_step_handler(message, add_image3, deck)


def add_image3(message, deck):
    if message.content_type == "photo":
        imageID = message.photo[-1].file_id
        image_info = bot.get_file(imageID)
        image_file = bot.download_file(image_info.file_path)
        bot.send_message(message.chat.id, "choose name")
        bot.register_next_step_handler(message, add_image4, deck, image_file)
    else:
        if message.text == "cancel":
            bot.send_message(message.chat.id, "ok", reply_markup=ReplyKeyboardRemove())
            return
        bot.send_message(message.chat.id, "wrong type")


def add_image4(message, deck, image_file):
    name = message.text
    try:
        with open(f"decks/{deck}/{name}.jpg", "wb") as f:
            f.write(image_file)
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(KeyboardButton("cancel"))
        bot.send_message(message.chat.id, "added an image, add another image to the deck?", reply_markup=markup)
        bot.register_next_step_handler(message, add_image3, deck)

    except:
        bot.send_message(message.chat.id, "something went wrong")


@bot.message_handler(commands=["deleteimage"])
def delete_image(message):
    abstract_choose_deck(message, delete_image2)


def delete_image2(message):
    deck = message.text
    if deck == "cancel":
        bot.send_message(message.chat.id, "ok", reply_markup=ReplyKeyboardRemove())
        return
    try:
        images = os.listdir(f"decks/{deck}")
        images.remove("statistics.json")
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        for image in images:
            markup.add(KeyboardButton(image[:image.index('.')]))
        markup.add(KeyboardButton("cancel"))
        bot.send_message(message.chat.id, "choose the image", reply_markup=markup)
        bot.register_next_step_handler(message, delete_image3, deck)
    except:
        bot.send_message(message.chat.id, "there is no such deck", reply_markup=ReplyKeyboardRemove())


def delete_image3(message, deck):
    image = message.text
    if image == "cancel":
        bot.send_message(message.chat.id, "ok", reply_markup=ReplyKeyboardRemove())
        return
    try:
        os.remove(f"decks/{deck}/{image}")
        bot.send_message(message.chat.id, "deleted an image", reply_markup=ReplyKeyboardRemove())
    except:
        bot.send_message(message.chat.id, "wrong name of image", reply_markup=ReplyKeyboardRemove())


@bot.message_handler(commands=["getimage"])
def get_image(message):
    abstract_choose_deck(message, get_image2)


def get_image2(message):
    deck = message.text
    if deck == "cancel":
        bot.send_message(message.chat.id, "ok", reply_markup=ReplyKeyboardRemove())
        return
    try:
        images = os.listdir(f"decks/{deck}")
        images.remove("statistics.json")
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        for image in images:
            markup.add(KeyboardButton(image[:image.index('.')]))
        markup.add(KeyboardButton("cancel"))
        bot.send_message(message.chat.id, "choose the image", reply_markup=markup)
        bot.register_next_step_handler(message, get_image3, deck)
    except:
        bot.send_message(message.chat.id, "wrong name of image", reply_markup=ReplyKeyboardRemove())


def get_image3(message, deck):
    image = message.text
    try:
        for file in os.listdir(f"decks/{deck}"):
            if file.startswith(image):
                image = file
                break
        with open(f"decks/{deck}/{image}", "rb") as file:
            bot.send_photo(message.chat.id, file, f"{image[:image.index('.')]}", reply_markup=ReplyKeyboardRemove())
    except:
        bot.send_message(message.chat.id, "wrong name of image", reply_markup=ReplyKeyboardRemove())


@bot.message_handler(commands=["train"])
def train(message):
    abstract_choose_deck(message, train2)


def train2(message):
    deck = message.text
    if deck == "cancel":
        bot.send_message(message.chat.id, "ok", reply_markup=ReplyKeyboardRemove())
        return
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("from text"))
    markup.add(KeyboardButton("from image"))
    markup.add(KeyboardButton("cancel"))
    bot.send_message(message.chat.id, "choose type", reply_markup=markup)
    bot.register_next_step_handler(message, train3, deck)


def train3(message, deck):
    typ = message.text
    if typ == "cancel":
        bot.send_message(message.chat.id, "ok", reply_markup=ReplyKeyboardRemove())
        return
    if typ not in ["from text", "from image"]:
        bot.send_message(message.chat.id, "wrong type", reply_markup=ReplyKeyboardRemove())
        return
    mas = os.listdir(f"decks/{deck}")
    mas.remove("statistics.json")
    shuffle(mas)
    train_text(message, deck, mas, typ)


def train_text(message, deck, mas, typ):
    if not mas:
        bot.send_message(message.chat.id, "there is nothing to train", reply_markup=ReplyKeyboardRemove())
        return
    image = mas.pop()
    params = {"image": image,
              "deck": deck,
              "typ": typ,
              "mas": mas,
              "correct": 0,
              "total": len(os.listdir(f"decks/{deck}"))-1}
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("view"))
    if params["typ"] == "from image":
        with open(f"decks/{deck}/{image}", "rb") as file:
            bot.send_photo(message.chat.id, file, reply_markup=markup, caption=f"{len(mas)} left")
    else:
        bot.send_message(message.chat.id, image[:image.index('.')] + " " + f"({len(mas)} left)", reply_markup=markup)
    bot.register_next_step_handler(message, view_text, params)


def view_text(message, params):
    if params["typ"] == "from image":
        bot.send_message(message.chat.id, params["image"][:params["image"].index('.')], reply_markup=ReplyKeyboardRemove())
    else:
        deck, image = params["deck"], params["image"]
        with open(f"decks/{deck}/{image}", "rb") as file:
            bot.send_photo(message.chat.id, file, reply_markup=ReplyKeyboardRemove())
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(KeyboardButton("Yes"), KeyboardButton("No"))
    markup.add(KeyboardButton("cancel"))
    bot.send_message(message.chat.id, "your answer was correct?", reply_markup=markup)
    bot.register_next_step_handler(message, train_text2, params)


def train_text2(message, params):
    ans = message.text
    if ans == "cancel":
        bot.send_message(message.chat.id, "ok", reply_markup=ReplyKeyboardRemove())
        return
    if ans not in ["Yes", "No"]:
        bot.send_message(message.chat.id, "wrong input", reply_markup=ReplyKeyboardRemove())
        return
    if ans == "Yes":
        params["correct"] += 1
        bot.send_message(message.chat.id, "good!", reply_markup=ReplyKeyboardRemove())
    else:
        bot.send_message(message.chat.id, "bad!", reply_markup=ReplyKeyboardRemove())
    if not params["mas"]:
        with open("decks/{}/{}".format(params["deck"], "statistics.json"), "r") as f:
            data = json.load(f)
            if data:
                bot.send_message(message.chat.id, "Your previous scores: {}".format(' '.join(data)), reply_markup=ReplyKeyboardRemove())
            score = str(round(params["correct"] / params["total"] * 100)) + "%"
            bot.send_message(message.chat.id, "Your score: {}".format(score), reply_markup=ReplyKeyboardRemove())
            data.append(score)
            if len(data) > 10:
                data = data[1:]
        with open("decks/{}/{}".format(params["deck"], "statistics.json"), "w") as f:
            f.write(json.dumps(data))
        return
    params["image"] = params["mas"].pop()
    with open("decks/{}/{}".format(params["deck"], params["image"]), "rb") as file:
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(KeyboardButton("view"))
        left = len(params["mas"])
        bot.send_photo(message.chat.id, file, reply_markup=markup, caption=f"{left} left")
        bot.register_next_step_handler(message, view_text, params)
    


def train_image(message, deck, mas):
    pass



bot.infinity_polling()