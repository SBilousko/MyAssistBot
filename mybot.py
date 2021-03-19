from bs4 import BeautifulSoup
import telebot, constants, functions, bot_token

bot = telebot.TeleBot(bot_token.token)

# bot.send_message(446340606, "Test")

# upd = bot.get_updates()

# last_upd = upd[-1]
# message_from_user = last_upd.message

# print(message_from_user)

print(bot.get_me())

def log(message, answer):
    print("\n --------")
    from datetime import datetime
    print(datetime.now())
    print("Повідомлення від {0} {1}. (id = {2}) \n Текст - {3}".format(message.from_user.first_name, message.from_user.last_name, str(message.from_user.id), message.text))
    print(answer)

@bot.message_handler(commands=["start"])
def handle_start(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    user_markup.row("/start", "/weather")
    user_markup.row("/currency", "/cryptoCurrency")
    # user_markup.row("Фото", "Аудіо", "Документи")
    # user_markup.row("Стікер", "Відео", "Голос", "Локація")
    bot.send_message(message.from_user.id, "Ласкаво просимо !!!", reply_markup=user_markup)

@bot.message_handler(commands=["weather"])
def handle_text(message):
    answer = functions.sinoptik_weather()[0] + "Прогноз на найближчі дні\n\n"  + functions.sinoptik_weather()[1]
    log(message, answer)
    bot.send_message(message.from_user.id, answer)

@bot.message_handler(commands=["currency"])
def handle_text(message):
    answer = functions.minfin_currency()
    log(message, answer)
    bot.send_message(message.from_user.id, answer)

@bot.message_handler(commands=["cryptoCurrency"])
def handle_text(message):
    answer = functions.minfin_crypto_currency()
    log(message, answer)
    bot.send_message(message.from_user.id, answer)

@bot.message_handler(commands=["stop"])
def handle_start(message):
    hide_markup = telebot.types.ReplyKeyboardHide()
    bot.send_message(message.from_user.id, "...", reply_markup=hide_markup)

bot.polling(none_stop=True, interval=0)