import telebot
import requests


TOKEN = "7869279278:AAH1wZEMPEyrcsweK5KJocVwyaegLRXkacY"
bot = telebot.TeleBot(TOKEN)
URL = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"


@bot.message_handler(commands=['start', 'help', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "hi im soheil what can I do for you?")

@bot.message_handler(func=lambda m: True)
def show_price(message):
    symbol = message.text.upper()
    response = requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}")
    if response.status_code == 200:
        data = response.json()
        bot.reply_to(message, f"{data['symbol']} price is {data['price']}")
    else:
        bot.reply_to(message, "Sorry, I don't understand your input")


bot.polling()