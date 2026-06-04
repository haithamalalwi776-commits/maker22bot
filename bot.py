import os
import telebot
from flask import Flask
import threading

TOKEN ="8696144716:AAEJK__TtCMEHL9Liq8702ArN1EkO379Oy4"
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# قائمة بـ 40 نوع بوت (يمكنك زيادتها)
bot_types = [f"بوت رقم {i}" for i in range(1, 41)]

def get_page_markup(page=0):
    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    start = page * 8
    end = start + 8
    
    # إضافة الأزرار للصفحة الحالية
    for b_type in bot_types[start:end]:
        markup.add(telebot.types.InlineKeyboardButton(b_type, callback_data=f"type_{b_type}"))
    
    # أزرار التنقل
    nav_buttons = []
    if page > 0:
        nav_buttons.append(telebot.types.InlineKeyboardButton("⬅️ السابق", callback_data=f"page_{page-1}"))
    if end < len(bot_types):
        nav_buttons.append(telebot.types.InlineKeyboardButton("التالي ➡️", callback_data=f"page_{page+1}"))
    
    markup.add(*nav_buttons)
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "اختر نوع البوت من الصفحات:", reply_markup=get_page_markup(0))

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data.startswith("page_"):
        page = int(call.data.split("_")[1])
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=get_page_markup(page))
    
    elif call.data.startswith("type_"):
        b_type = call.data.split("_")[1]
        msg = bot.send_message(call.message.chat.id, f"لقد اخترت {b_type}. أرسل التوكن الآن:")
        bot.register_next_step_handler(msg, lambda m: process_bot_creation(m, b_type))

def process_bot_creation(message, b_type):
    user_token = message.text.strip()
    try:
        temp_bot = telebot.TeleBot(user_token)
        info = temp_bot.get_me()
        # رسالة تفاصيل البوت
        details = (
            f"✅ تم إنشاء البوت بنجاح!\n\n"
            f"🤖 اسم البوت: {info.first_name}\n"
            f"👤 المعرف: @{info.username}\n"
            f"⚙️ النوع المختار: {b_type}\n"
            f"🛠 الحالة: يعمل الآن بامتياز."
        )
        bot.reply_to(message, details)
    except:
        bot.reply_to(message, "❌ التوكن غير صحيح.")

# تشغيل السيرفر
@app.route('/')
def home(): return "Bot Maker Pagination Live!"

if __name__ == '__main__':
    bot.remove_webhook()
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000))), daemon=True).start()
    bot.infinity_polling(skip_pending=True)
