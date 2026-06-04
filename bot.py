import os
import telebot
from flask import Flask
import threading

# ضع التوكن الجديد الخاص بك هنا
BOT_TOKEN ="8283760934:AAFL65dKFkzgGsShWlQXyPo0yLf875dXzio "
bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# إنشاء قائمة بـ 40 بوت
bot_types = [f"بوت رقم {i}" for i in range(1, 41)]

def get_page_markup(page=0):
    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    start, end = page * 8, (page + 1) * 8
    
    # إضافة الأزرار للصفحة الحالية (8 أزرار لكل صفحة)
    for b_type in bot_types[start:end]:
        markup.add(telebot.types.InlineKeyboardButton(b_type, callback_data=f"type_{b_type}"))
    
    # أزرار التنقل
    nav = []
    if page > 0: nav.append(telebot.types.InlineKeyboardButton("⬅️", callback_data=f"page_{page-1}"))
    if end < len(bot_types): nav.append(telebot.types.InlineKeyboardButton("➡️", callback_data=f"page_{page+1}"))
    markup.row(*nav)
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "مرحباً! اختر نوع البوت الذي تريده:", reply_markup=get_page_markup(0))

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data.startswith("page_"):
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=get_page_markup(int(call.data.split("_")[1])))
    elif call.data.startswith("type_"):
        b_type = call.data.split("_")[1]
        msg = bot.send_message(call.message.chat.id, f"تم اختيار {b_type}. أرسل توكن الب
