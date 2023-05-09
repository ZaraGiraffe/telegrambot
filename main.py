import telebot

def token():
    return "5103709864:AAF1XqfUBGIKAzmT0IEeQOMBSg7Ic6FFDjU"

bot = telebot.TeleBot(token())

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Howdy, how are you doing?")

@bot.message_handler(func=lambda m: True)
def echo_all(message):
      bot.reply_to(message, "hello")

bot.infinity_polling()