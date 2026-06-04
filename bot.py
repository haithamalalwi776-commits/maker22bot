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

BOT_TOKEN = "8283760934:AAHn2rrYm3INlJa01qnCe9UGi_tGrMpZm00"
bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

bot_types = ["بوت تواصل", "صارحني", "اكس او"]

@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    for b in bot_types: markup.add(b)
    msg = bot.send_message(message.chat.id, "🎯 أهلاً بك، اختر نوع البوت:", reply_markup=markup)
    bot.register_next_step_handler(msg, ask_token)

def ask_token(message):
    b_type = message.text
    if b_type not in bot_types:
        bot.reply_to(message, "❌ اختر من القائمة.")
        return
    msg = bot.send_message(message.chat.id, "✅ أرسل توكن البوت:")
    bot.register_next_step_handler(msg, lambda m: deploy_bot(m, b_type))

def deploy_bot(message, b_type):
    token = message.text.strip()
    cursor.execute('INSERT INTO bots VALUES (?, ?, ?)', (message.chat.id, token, b_type))
    conn.commit()
    
    # القالب الآن موجود في المجلد الرئيسي مباشرة
    script = "contact.py"
    
    if os.path.exists(script):
        subprocess.Popen(["python3", script, token])
        bot.reply_to(message, f"🚀 تم تفعيل بوت '{b_type}' بنجاح!")
    else:
        bot.reply_to(message, "⚠️ خطأ: ملف القالب غير موجود في المجلد الرئيسي.")

@app.route('/')
def home(): return "Bot Maker Platform Running"

if __name__ == '__main__':
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=10000)).start()
    bot.infinity_polling()
 
