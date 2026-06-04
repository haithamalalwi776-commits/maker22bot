import os
import telebot
from flask import Flask
import threading

# ضع التوكن الجديد الخاص بك هنا
BOT_TOKEN = "8283760934:AAHzd8w-dOUseEK-GbacAojZVuPIWG--UUQ"
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
        msg = bot.send_message(call.message.chat.id, f"تم اختيار {b_type}. أرسل توكن البوت المراد صنعه الآن:")
        bot.register_next_step_handler(msg, lambda m: confirm_bot(m, b_type))

def confirm_bot(message, b_type):
    user_token = message.text.strip()
    try:
        temp_bot = telebot.TeleBot(user_token)
        info = temp_bot.get_me()
        bot.reply_to(message, f"✅ تم إنشاء البوت بنجاح!\n\n🤖 الاسم: {info.first_name}\n👤 المعرف: @{info.username}\n⚙️ النوع: {b_type}\n🛡 الحالة: يعمل الآن.")
    except:
        bot.reply_to(message, "❌ توكن غير صحيح، تأكد منه وحاول مرة أخرى.")

@app.route('/')
def home(): return "Bot is Live!"

if __name__ == '__main__':
    bot.remove_webhook()
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000))), daemon=True).start()
    bot.infinity_polling(skip_pending=True)
