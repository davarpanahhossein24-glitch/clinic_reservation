import telebot
import requests

TOKEN = "7869279278:AAH1wZEMPEyrcsweK5KJocVwyaegLRXkacR" # فقط برای نمونه، توکن شما رو عوض کردم
bot = telebot.TeleBot(TOKEN)

# این URL رو دیگه نیازی نیست اینجا تعریف کنید چون داخل تابع ساخته میشه
# URL = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"

@bot.message_handler(commands=['start', 'help', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Hi, I'm Soheil. I can fetch cryptocurrency prices for you. Just send me a trading pair like BTCUSDT, or use /price BTCUSDT.")

# این هندلر برای دریافت قیمت ارزهاست
@bot.message_handler(func=lambda message: True) # این خط هر پیامی رو هندل میکنه
def show_price(message):
    text = message.text.strip().upper() # حذف فاصله‌های اضافی و تبدیل به حروف بزرگ

    # اگر کاربر با /price شروع کرده باشه
    if text.startswith('/PRICE '):
        symbol = text.replace('/PRICE ', '')
    else:
        symbol = text # در غیر این صورت، کل متن رو به عنوان symbol در نظر می‌گیریم

    # یک بررسی اولیه برای اینکه مطمئن شیم symbol فرمت درستی داره
    # مثلاً فقط شامل حروف و اعداد باشه و طولش منطقی باشه
    if not (4 <= len(symbol) <= 10 and symbol.isalnum()): # مثال: طول بین 4 تا 10 و فقط حروف و اعداد
        bot.reply_to(message, "Please enter a valid cryptocurrency trading pair (e.g., BTCUSDT).")
        return

    try:
        response = requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}")
        response.raise_for_status() # این خط اگر وضعیت HTTP کد خطا (مثل 4xx یا 5xx) باشه، یک استثنا ایجاد میکنه

        data = response.json()
        if 'code' in data and 'msg' in data: # بایننس برای symbol نامعتبر، یک JSON با 'code' و 'msg' برمی‌گردونه
            bot.reply_to(message, f"Error: {data['msg']}. Please check the trading pair. (e.g., BTCUSDT)")
        elif 'symbol' in data and 'price' in data:
            bot.reply_to(message, f"{data['symbol']} price is {float(data['price']):.8f}") # فرمت کردن قیمت
        else:
            bot.reply_to(message, "Could not retrieve price. Please try again later or check the symbol.")

    except requests.exceptions.RequestException as e:
        bot.reply_to(message, f"There was an issue connecting to the exchange: {e}. Please try again later.")
    except Exception as e:
        bot.reply_to(message, f"An unexpected error occurred: {e}. Please contact support if the issue persists.")


print("Bot is running...")
bot.polling()