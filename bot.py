import os
import telebot
from flask import Flask
import threading

BOT_TOKEN ="8283760934:AAHzd8w-dOUseEK-GbacAojZVuPIWG--UUQ"
bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# القاموس الذي يربط اسم البوت بملف الكود الخاص به
bot_scripts = {
    "بوت تواصل": "codes/contact.py",
    "صارحني": "codes/sarahah.py",
    "اكس او": "codes/xo.py",
    # أضف هنا مسارات جميع الملفات
}

def get_markup(page=0):
    # (نفس نظام الصفحات السابق)
    # ...
    pass

@bot.callback_query_handler(func=lambda call: call.data.startswith("type_"))
def handle_type(call):
    b_type = call.data.split("_")[1]
    msg = bot.send_message(call.message.chat.id, f"أرسل توكن البوت لتفعيل نوع: {b_type}")
    bot.register_next_step_handler(msg, lambda m: deploy_bot(m, b_type))

def deploy_bot(message, b_type):
    token = message.text.strip()
    script_path = bot_scripts.get(b_type)
    
    # هنا الجزء الاحترافي: بوت الصانع يقوم بتشغيل كود البوت الجديد
    # ملاحظة: في بيئة Render، يفضل استخدام Database لتخزين التوكنات 
    # وتشغيل كل بوت كـ Process منفصل باستخدام subprocess
    bot.reply_to(message, f"✅ تم تفعيل {b_type}!\nجاري تشغيل البوت الآن...")
    os.system(f"python {script_path} {token} &")

# الجزء الخاص بالسيرفر
@app.route('/')
def home(): return "Bot Maker Platform Active"

if __name__ == '__main__':
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=10000)).start()
    bot.infinity_polling()
 
