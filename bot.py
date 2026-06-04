import telebot
from telebot import types
import threading
import os
from threading import Thread
from flask import Flask

# إنشاء تطبيق ويب وهمي لإرضاء سيرفر Render
app = Flask('')

@app.route('/')
def home():
    return "Bot is Running Live!"

def run():
    # Render يرسل المنفذ تلقائياً في متغير PORT، وإذا لم يجده يفتح على 8080
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# تشغيل موقع الويب الوهمي في خلفية البوت دون التأثير عليه
Thread(target=run).start()

# ⚠️ ضع توكين بوتك الرئيسي الشغال هنا
MAIN_BOT_TOKEN ="8696144716:AAGphvaLzcfnO7xr6OuEDnblo70MSogd01E"
main_bot = telebot.TeleBot(MAIN_BOT_TOKEN)

active_bots = {}

# قائمة الـ 40 بوتاً التي طلبتها (يمكنك تعديل أسمائها لاحقاً كما تحب)
ALL_BOTS = [
    {"id": "twasol", "name": "✉️ بوت تواصل"},
    {"id": "rps", "name": "🪨 حجرة ورقة مقص"},
    {"id": "sarahni", "name": "🎭 بوت صارحني"},
    {"id": "comments", "name": "💬 بوت تعليقات"},
    {"id": "roulette", "name": "🎰 بوت روليت"},
    {"id": "xo", "name": "❌ بوت إكس أو (XO)"},
    {"id": "download", "name": "📥 تحميل ميديا"},
    {"id": "apple_ai", "name": "🍏 ذكاء تفاح صناعي"},
    {"id": "quran", "name": "📖 بوت القرآن الكريم"},
    {"id": "اذكار", "name": "📿 بوت الأذكار"},
    {"id": "games_group", "name": "🧩 ألعاب المجموعات"},
    {"id": "welcome_bot", "name": "👋 بوت الترحيب والتقييد"},
    {"id": "trans", "name": "🌐 بوت الترجمة الفورية"},
    {"id": "weather", "name": "🌤️ بوت الطقس"},
    {"id": "currency", "name": "💰 تحويل العملات"},
    {"id": "pdf_bot", "name": "📄 تحويل ملفات PDF"},
    {"id": "links", "name": "🔗 اختصار الروابط"},
    {"id": "anime", "name": "🎬 بوت الأنمي"},
    {"id": "movies", "name": "🍿 بوت الأفلام"},
    {"id": "stories", "name": "📚 بوت قصص وروايات"},
    {"id": "instagram", "name": "📸 تحميل انستغرام"},
    {"id": "tiktok", "name": "🎵 تحميل تيك توك"},
    {"id": "youtube", "name": "🎥 تحميل يوتيوب"},
    {"id": "twitter", "name": "🐦 تحميل تويتر"},
    {"id": "management", "name": "⚙️ إدارة المجموعات"},
    {"id": "muting", "name": "🔇 كتم وتثبيت التلقائي"},
    {"id": "numbers", "name": "🔢 بوت الأرقام وهمية"},
    {"id": "stickers", "name": "🖼️ صانع الملصقات"},
    {"id": "voice", "name": "🎙️ تحويل الصوت لنص"},
    {"id": "text_voice", "name": "🗣️ تحويل النص لصوت"},
    {"id": "anonymous", "name": "👥 شات عشوائي تعارف"},
    {"id": "truth", "name": "❓ لعبة صراحة أو جرأة"},
    {"id": "calculator", "name": "🧮 بوت الحاسبة الذكية"},
    {"id": "notes", "name": "📝 بوت حفظ الملاحظات"},
    {"id": "remind", "name": "⏰ بوت التذكير بالمهام"},
    {"id": "rules", "name": "📜 قوانين المجموعات"},
    {"id": "search_bot", "name": "🔍 بوت البحث في جوجل"},
    {"id": "hash", "name": "🔐 تشفير النصوص"},
    {"id": "games_sub", "name": "🕹️ بوت ألعاب المطور"},
    {"id": "support", "name": "🛠️ الدعم الفني للمصانع"}
]

ITEMS_PER_PAGE = 8

# دالة توليد الأزرار بناءً على رقم الصفحة
def generate_keyboard(page=0):
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    # حساب البداية والنهاية للصفحة الحالية
    start_idx = page * ITEMS_PER_PAGE
    end_idx = start_idx + ITEMS_PER_PAGE
    page_items = ALL_BOTS[start_idx:end_idx]
    
    # إضافة أزرار البوتات لـ الصفحة الحالية
    for bot in page_items:
        markup.add(types.InlineKeyboardButton(bot["name"], callback_data=f"make_{bot['id']}"))
    
    # أزرار التنقل (السابق والتالي)
    nav_buttons = []
    if page > 0:
        nav_buttons.append(types.InlineKeyboardButton("⬅️ السابق", callback_data=f"page_{page-1}"))
    if end_idx < len(ALL_BOTS):
        nav_buttons.append(types.InlineKeyboardButton("التالي ➡️", callback_data=f"page_{page+1}"))
        
    if nav_buttons:
        markup.add(*nav_buttons)
        
    return markup

# تشغيل البوت الفرعي (المحرك الداخلي)
def start_user_bot(user_token, bot_type):
    try:
        sub_bot = telebot.TeleBot(user_token)
        @sub_bot.message_handler(commands=['start'])
        def welcome(message):
            sub_bot.reply_to(message, f"مرحباً بك! تم تشغيلي بنجاح كـ بوت مخصص من النوع المختار.")
        sub_bot.infinity_polling()
    except Exception as e:
        print(f"خطأ في البوت الفرعي: {e}")

# عند إرسال /start تظهر الصفحة الأولى (أول 8 بوتات)
@main_bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = generate_keyboard(page=0)
    main_bot.reply_to(message, "مرحباً بك في مصنع البوتات العملاق! 🤖🔥\n\nتصفح الأزرار بالأسفل واختر البوت الذي تريد إنشاءه (تنقل عبر الصفحات):", reply_markup=markup)

# معالجة أزرار التنقل بين الصفحات
@main_bot.callback_query_handler(func=lambda call: call.data.startswith("page_"))
def handle_pagination(call):
    page = int(call.data.split("_")[1])
    markup = generate_keyboard(page=page)
    main_bot.edit_message_text(
        "تصفح الأزرار بالأسفل واختر البوت الذي تريد إنشاءه (تنقل عبر الصفحات):",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=markup
    )

# معالجة اختيار أحد الـ 40 بوتاً
@main_bot.callback_query_handler(func=lambda call: call.data.startswith("make_"))
def callback_inline(call):
    bot_type = call.data.replace("make_", "")
    
    # جلب اسم البوت المختار من القائمة
    chosen_bot = next((b for b in ALL_BOTS if b["id"] == bot_type), None)
    bot_name = chosen_bot["name"] if chosen_bot else "بوت مخصص"
    
    msg = main_bot.send_message(
        call.message.chat.id, 
        f"لقد اخترت إنشاء [{bot_name}] 🛠️\n\nمن فضلك أرسل الآن توكين (Token) البوت الجديد من @BotFather:"
    )
    main_bot.register_next_step_handler(msg, lambda m: handle_token(m, bot_type))

def handle_token(message, bot_type):
    token = message.text.strip()
    
    if ":" not in token or len(token) < 35:
        main_bot.reply_to(message, "❌ التوكين غير صحيح! أرسل /start مجدداً وجرب مرة أخرى.")
        return

    if token in active_bots:
        main_bot.reply_to(message, "⚠️ هذا البوت يعمل بالفعل على السيرفر!")
        return

    main_bot.reply_to(message, f"🔄 جاري بناء تشكيلة الملفات وتفعيل بوتك تلقائياً...")

    t = threading.Thread(target=start_user_bot, args=(token, bot_type))
    t.daemon = True
    t.start()

    active_bots[token] = t
    main_bot.reply_to(message, f"✅ تم تشغيل البوت بنجاح! اذهب إليه الآن لتجربته.")

if __name__ == '__main__':
    print("🤖 بوت الصانع العملاق (40 زرار) يعمل الآن بنجاح...")
    main_bot.infinity_polling()
