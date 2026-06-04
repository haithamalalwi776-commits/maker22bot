 import telebot
import sqlite3
import subprocess
from flask import Flask
import threading
import os

# إعداد قاعدة البيانات
conn = sqlite3.connect('bots_data.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS bots (user_id INTEGER, token TEXT, bot_type TEXT)')
conn.commit()

# توكن بوت الصانع (ضعه هنا)
BOT_TOKEN = "8283760934:AAHn2rrYm3INlJa01qnCe9UGi_tGrMpZm00"
bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

bot_types = ["بوت تواصل", "صارحني", "اكس او"]

@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    for b in bot_types: markup.add(b)
    msg = bot.send_message(message.chat.id, "🎯 أهلاً بك في منصة الصانع، اختر نوع البوت:", reply_markup=markup)
    bot.register_next_step_handler(msg, ask_token)

def ask_token(message):
    b_type = message.text
    if b_type not in bot_types:
        bot.reply_to(message, "❌ اختر من القائمة من فضلك.")
        return
    msg = bot.send_message(message.chat.id, "✅ أرسل توكن البوت الجديد لتفعيله:")
    bot.register_next_step_handler(msg
 
