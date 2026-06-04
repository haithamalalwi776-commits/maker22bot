import telebot
import sqlite3
from flask import Flask
import threading
import os

# إعداد قاعدة البيانات
conn = sqlite3.connect('bots_data.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS bots (user_id INTEGER, token TEXT, bot_type TEXT)')
conn.commit()

bot = telebot.TeleBot("8283760934:AAHn2rrYm3INlJa01qnCe9UGi_tGrMpZm00")
app = Flask(__name__)

# قائمة أنواع البوتات
bot_types = ["بوت تواصل", "صارحني", "حجرة ورقة مقص", "اكس او", "بوت التفاح"]

@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    for b in bot_types: markup.add(b)
    msg = bot.send_message(message.chat.id, "🎯 أهلاً بك! اختر نوع البوت الذي تريد صنعه من القائمة:", reply_markup=markup)
    bot.register_next_step_handler(msg, ask_token)

def ask_token(message):
    b_type = message.text
    if b_type not in bot_types:
        bot.reply_to(message, "❌ يرجى اختيار نوع من القائمة.")
        return
    msg = bot.send_message(message.chat.id, f"✅ تم اختيار '{b_type}'.\n\nأرسل الآن 'التوكن' الخاص بالبوت الجديد:")
    bot.register_next_step_handler(msg, lambda m: save_bot_data(m, b_type))

def save_bot_data(message, b_type):
    token = message.text.strip()
    user_id = message.chat.id
    cursor.execute('INSERT INTO bots VALUES (?, ?, ?)', (user_id, token, b_type))
    conn.commit()
    bot.reply_to(message, f"🎉 تم حفظ بيانات بوت '{b_type}' بنجاح في قاعدة البيانات!\n\nقريباً سيتم تفعيله.")

@app.route('/')
def home(): return "Bot Maker Platform Active"

if __name__ == '__main__':
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=10000)).start()
    bot.infinity_polling()
 
