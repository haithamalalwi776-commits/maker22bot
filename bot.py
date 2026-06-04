import os
import threading
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

TOKEN ="8696144716:AAEJK__TtCMEHL9Liq8702ArN1EkO379Oy4" 
ADMIN_ID = 123456789 # ID حقك من @userinfobot

app = Flask('')
@app.route('/')
def home(): return "مصنع البوتات شغال 24/7 ✅"
def run_flask(): app.run(host='0.0.0.0', port=8080)

# قاعدة بيانات البوتات المصنوعة
bots_db = {}

# 40 زر جاهز للتقسيم
BUTTONS_40 = [
    {"text": f"زر {i+1}", "data": f"btn_{i+1}"}
    for i in range(40)
]

def paginate_buttons(buttons, page=0, per_page=8):
    """تقسيم الأزرار صفحات"""
    start = page * per_page
    end = start + per_page
    page_buttons = buttons[start:end]

    keyboard = []
    # صفين أزرار، كل صف 4 أزرار
    for i in range(0, len(page_buttons), 4):
        row = [
            InlineKeyboardButton(b["text"], callback_data=b["data"])
            for b in page_buttons[i:i+4]
        ]
        keyboard.append(row)

    # أزرار التنقل
    nav = []
    if page > 0:
        nav.append(InlineKeyboardButton("⬅️ السابق", callback_data=f"page_{page-1}"))
    if end < len(buttons):
        nav.append(InlineKeyboardButton("التالي ➡️", callback_data=f"page_{page+1}"))
    if nav:
        keyboard.append(nav)

    keyboard.append([InlineKeyboardButton("🏠 الرئيسية", callback_data="home")])
    return InlineKeyboardMarkup(keyboard)

def generate_bot_code(bot_name, token_placeholder="TOKEN_HERE"):
    """يولد كود بوت كامل فيه 40 زر بصفحات"""
    return f'''import threading
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "{token_placeholder}"
app = Flask('')
@app.route('/')
def home(): return "{bot_name} شغال 24/7"
def run_flask(): app.run(host='0.0.0.0', port=8080)

BUTTONS = {BUTTONS_40}

def paginate(page=0, per_page=8):
    start = page * per_page
    end = start + per_page
    page_btns = BUTTONS[start:end]
    keyboard = []
    for i in range(0, len(page_btns), 4):
        row = [InlineKeyboardButton(b["text"], callback_data=b["data"]) for b in page_btns[i:i+4]]
        keyboard.append(row)
    nav = []
    if page > 0: nav.append(InlineKeyboardButton("⬅️ السابق", callback_data=f"p{{page-1}}"))
    if end < len(BUTTONS): nav.append(InlineKeyboardButton("التالي ➡️", callback_data=f"p{{page+1}}"))
    if nav: keyboard.append(nav)
    keyboard.append([InlineKeyboardButton("🏠 الرئيسية", callback_data="home")])
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "مرحبا! اختر من القائمة:",
        reply_markup=paginate(0)
    )

async def buttons_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data.startswith("p"):
        page = int(query.data[1:])
        await query.edit_message_text("اختر:", reply_markup=paginate(page))
    elif query.data == "home":
        await query.edit_message_text("الرئيسية:", reply_markup=paginate(0))
    else:
        await query.answer(f"ضغطت {query.data} ✅", show_alert=True)

if __name__ == '__main__':
    threading.Thread(target=run_flask, daemon=True).start()
    app_bot = ApplicationBuilder().token(TOKEN).build()
    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(CallbackQueryHandler(buttons_handler))
    app_bot.run_polling()
'''

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id!= ADMIN_ID:
        return await update.message.reply_text("ممنوع ❌")

    keyboard = [
        [InlineKeyboardButton("➕ صنع بوت جديد", callback_data='newbot')],
        [InlineKeyboardButton("📋 البوتات المصنوعة", callback_data='listbots')],
        [InlineKeyboardButton("ℹ️ المساعدة", callback_data='help')]
    ]
    await update.message.reply_text(
        "🤖 مصنع البوتات الاحترافي\n"
        "اصنع 40+ بوت، كل بوت 40 زر بصفحات\n"
        "اختر:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def new_bot_flow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text(
        "اكتب اسم البوت الجديد:\n"
        "مثال: /create bot_store"
    )
    context.user_data['waiting_name'] = True

async def create_bot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id!= ADMIN_ID:
        return

    args = context.args
    if not args:
        return await update.message.reply_text("اكتب: /create اسم_البوت")

    bot_name = args[0]

    # يولد الكود
    code = generate_bot_code(bot_name)

    # يحفظ الملف
    filename = f"{bot_name}.py"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(code)

    bots_db[bot_name] = {"file": filename, "status": "جاهز"}

    await update.message.reply_text(
        f"✅ تم صنع {bot_name}.py\n"
        f"الخطوات:\n"
        f"1. روح @BotFather وسوي بوت جديد\n"
        f"2. انسخ التوكن\n"
        f"3. افتح ملف {filename} وغير TOKEN_HERE\n"
        f"4. شغل: python {filename}\n"
        f"5. ارفعه ريبل + بورت 8080 عشان 24 ساعة",
        parse_mode='Markdown'
    )

async def list_bots(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if not bots_db:
        return await query.message.reply_text("ما عندك بوتات مصنوعة لسه")

    text = "📋 البوتات المصنوعة:\n\n"
    for name, info in bots_db.items():
        text += f"• {name} - {info['status']}\n"

    await query.message.reply_text(text)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'newbot':
        await new_bot_flow(update, context)
    elif query.data == 'listbots':
        await list_bots(update, context)
    elif query.data == 'help':
        await query.message.reply_text(
            "طريقة الاستخدام:\n"
            "1. /create اسم_البوت → يولد ملف بايثون\n"
            "2. حط التوكن في الملف\n"
            "3. شغله على ريبل\n"
            "كل بوت يجي فيه 40 زر مقسمة 5 صفحات، 8 أزرار بالصفحة"
        )

if __name__ == '__main__':
    threading.Thread(target=run_flask, daemon=True).start()

    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("create", create_bot))
    application.add_handler(CallbackQueryHandler(button_handler))

    print("مصنع البوتات شغال...")
    application.run_polling() 
