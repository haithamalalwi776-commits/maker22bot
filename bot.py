import os
import threading
from flask import Flask
import telebot
from telebot import types

# ---------------------------------------------------------
# 1. كود Flask الوهمي لاستقرار السيرفر على Render
# ---------------------------------------------------------
app = Flask(__name__)

@app.route('/')
def home():
    return "Multi-Bot Maker Server is Running Live!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

threading.Thread(target=run_flask, daemon=True).start()

# ---------------------------------------------------------
# 2. إعداد البوت الصانع الرئيسي
# ---------------------------------------------------------
BOT_TOKEN = "8696144716:AAFF9SU0uXoSgtmTtAkWwaFBpAXXNZ_BWoU"
bot = telebot.TeleBot(BOT_TOKEN)

# قاموس لحفظ نوع البوت الذي يختاره كل مستخدم مؤقتاً
user_choices = {}

# قائمة الأزرار والأنواع المتوفرة في البوت
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    # هنا يمكنك إضافة أو تغيير أي أزرار وأنواع تريدها مستقبلاً
    btn1 = types.InlineKeyboardButton("🔄 بوت تواصل", callback_data="type_بوت تواصل")
    btn2 = types.InlineKeyboardButton("🛡️ بوت حماية للمجموعات", callback_data="type_بوت حماية المجموعات")
    btn3 = types.InlineKeyboardButton("🎯 بوت ألعاب وفقرات", callback_data="type_بوت ألعاب وفقرات")
    btn4 = types.InlineKeyboardButton("📢 بوت نشر تلقائي", callback_data="type_بوت نشر تلقائي")
    
    markup.add(btn1, btn2, btn3, btn4)
    
    welcome_text = (
        "👋 أهلاً بك في بوت صانع البوتات المطور!\n\n"
        "🤖 يرجى اختيار نوع البوت الذي ترغب في صناعته من الأزرار أدناه 👇"
    )
    bot.reply_to(message, welcome_text, reply_markup=markup)

# استقبال ضغطة أي زر وتحديد النوع تلقائياً
@bot.callback_query_handler(func=lambda call: call.data.startswith("type_"))
def handle_bot_selection(call):
    # استخراج اسم النوع من الزر المضغوط
    selected_type = call.data.split("_")[1]
    user_choices[call.message.chat.id] = selected_type
    
    msg = bot.send_message(
        call.message.chat.id, 
        f"📥 رائع! لقد اخترت صناعة (**{selected_type}**).\n\n"
        f"قم بإرسال **التوكن (Token)** الخاص بالبوت الآن من @BotFather:"
    )
    bot.register_next_step_handler(msg, process_token)

# معالجة التوكن وإظهار الرسالة الموحدة حسب نوع الزر
def process_token(message):
    user_token = message.text.strip()
    chat_id = message.chat.id
    
    # جلب نوع البوت الذي اختاره المستخدم من الزر، وإذا لم يجد يضع افتراضي "تواصل"
    bot_type = user_choices.get(chat_id, "بوت تواصل")
    
    try:
        # فحص التوكن وجلب معرف البوت المصنوع
        temp_bot = telebot.TeleBot(user_token)
        bot_info = temp_bot.get_me()
        bot_username = f"@{bot_info.username}"
        
        # تشغيل وهمي خفيف للبوت المصنوع ليبقى "يعمل الآن"
        @temp_bot.message_handler(commands=['start'])
        def echo_start(m):
            temp_bot.reply_to(m, f"مرحباً بك! هذا البوت تم إنشاؤه بنجاح كـ {bot_type}.")
            
        threading.Thread(target=lambda: temp_bot.infinity_polling(skip_pending=True), daemon=True).start()

        # الرسالة الموحدة الفخمة (تتغير فيها كلمة "النوع" ديناميكياً حسب الزر المختار)
        success_message = (
            f"✨\n"
            f"🎉 تهانينا! تم إنشاء البوت بنجاح\n\n"
            f"✅ الخطوة 3 من 3: البوت جاهز للاستخدام\n\n"
            f"🤖 معلومات البوت:\n"
            f"• النوع: {bot_type} 🔄\n"
            f"• المعرف: {bot_username}\n"
            f"• الحالة: ✅ يعمل الآن\n\n"
            f"━━━━━━━━━━━━━━━\n"
            f"📌 الخطوات التالية:\n\n"
            f"1️⃣ جرّب البوت: افتحه من {bot_username}\n"
            f"2️⃣ خصص البوت: غيّر الاسم والصورة\n"
            f"3️⃣ انشر البوت: شارك الرابط مع الأصدقاء\n\n"
            f"💡 نصيحة: يمكنك تخصيص اسم وصورة البوت من @BotFather"
        )
        bot.send_message(chat_id, success_message)

    except Exception as e:
        bot.send_message(chat_id, "❌ عذراً، التوكن الذي أرسلته غير صحيح! يرجى التأكد وإعادة المحاولة.")
