import telebot
import sqlite3
import os
from flask import Flask
import threading

# إعداد قاعدة البيانات
conn = sqlite3.connect('bots_data.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS bots (user_id INTEGER, token TEXT, bot_type TEXT)')
conn.commit()

bot = telebot.TeleBot("8283760934:AAHn2rrYm3INlJa01qnCe9UGi_tGrMpZm00")
app = Flask(__name__)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "أهلاً بك! أرسل توكن البوت الذي تريد صنعه:")
    bot.register_next_step_handler(message, ask_type)

def ask_type(message):
    token = message.text
    msg = bot.send_message(message.chat.id, "اختر نوع البوت (مثلاً: تواصل):")
    bot.register_next_step_handler(msg, lambda m: save_bot(m, token))

def save_bot(message, token):
    bot_type = message.text
    cursor.execute('INSERT INTO bots VALUES (?, ?, ?)', (message.chat.id, token, bot_type))
    conn.commit()
    bot.reply_to(message, f"✅ تم حفظ بيانات البوت نوع: {bot_type} بنجاح!")

@app.route('/')
def home(): return "Bot Maker is ON"

if __name__ == '__main__':
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=10000)).start()
    bot.infinity_polling()
 
