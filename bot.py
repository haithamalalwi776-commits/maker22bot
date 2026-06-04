import os
import subprocess
import sys

# تثبيت المكتبات تلقائياً إذا لم تكن موجودة
try:
    import telebot
    import flask
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyTelegramBotAPI", "flask"])
    import telebot
    import flask

# إعداد البوت
BOT_TOKEN = "8283760934:AAGJ-ztigJuAWWJdOMENM9qqYBfO9yxrrq0" 
bot = telebot.TeleBot(BOT_TOKEN)
app = flask.Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

if __name__ == "__main__":
    import threading
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))).start()
    bot.remove_webhook()
    bot.infinity_polling(skip_pending=True)
