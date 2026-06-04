import os
import telebot
import time
from flask import Flask
import threading

# 1. إعداد التوكن
BOT_TOKEN ="8696144716:AAETqWYkCaK08gB5s-yp-l8fI4VZ2VxVQGw" 
bot = telebot.TeleBot(BOT_TOKEN)

# 2. إعداد سيرفر الويب لاستقرار رندر
app = Flask(__name__)
@app.route('/')
def home():
    return "Bot is running perfectly!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# 3. إعداد الأزرار
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        telebot.types.InlineKeyboardButton("🔄 بوت تواصل", callback_data="type_tawasul"),
        telebot.types.InlineKeyboardButton("🛡️ بوت حماية", callback_data="type_himaya"),
        telebot.types.InlineKeyboardButton("🎯 بوت ألعاب", callback_data="type_al3ab"),
        telebot.types.InlineKeyboardButton("📢 بوت نشر", callback_data="type_nashr")
    )
    bot.reply_to(message, "أ
 
