import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters
)

# Кроки анкети
(LANG, INSTAGRAM, AGE, WHY, OUTFIT, HELP, WISHES, PUBLIC, QUESTIONS) = range(9)

# Запитання
questions_uk = [
    "Ім'я:",
    "Нік в Instagram (або посилання на сторінку):",
    "Вік:",
    "Чому тебе цікавить ця зйомка? (кілька слів, не обов'язково серйозно):",
    "Який образ/одяг плануєш?",
    "Чи потрібна допомога з вибором одягу/образу? (так/ні):",
    "Чи маєш побажання до зйомки? (Наприклад: хочу більше портретів, люблю знімки в русі тощо):",
    "Чи комфортно тобі, якщо фото потраплять у публічне портфоліо/Instagram? (так/ні):"
]

questions_en = [
    "Name:",
    "Instagram nick (or link to your page):",
    "Age:",
    "Why are you interested in this photoshoot? (a few words, doesn't have to be serious):",
    "What look/outfit do you plan to wear?",
    "Do you need help choosing clothes/look? (yes/no):",
    "Do you have any wishes for the shoot? (e.g. I want more portraits, I like shots in motion, etc.):",
    "Are you comfortable if photos appear in public portfolio/Instagram? (yes/no):"
]

# ⚠️ ВСТАВ свій реальний chat_id
MY_CHAT_ID = 1165164756

# Старт
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['answers'] = {}
    context.user_data['lang'] = None

    message = (
        "Ми вирішили створити спільний проєкт — не просто серію знімків, а простір, де перетинаються наші бачення. "
        "Це індивідуальна фотосесія. З вами буде працювати два фотографи. "
        "Різне бачення, різна подача — одна ідея.\n\n"
        "📋 *Деталі:* \n"
        "• Час зйомки: 30 хвилин\n"
        "• Два фотографи (моя сторінка та Ліди)\n"
        "• Кількість місць обмежена\n"
        "• Ціна: 150 Cad\n"
        "• Серце зйомки — ретро автомобіль 🚗\n\n"
        "📌 *Це ПРЕ-запис.* Точну дату та місце ми повідомимо, коли зберемо необхідну кількість учасників!\n\n"
        "---\n\n"
        "We decided to create a shared project — not just a series of shots, but a space where our visions intersect. "
        "This is an individual photoshoot. You’ll be working with two photographers. "
        "Different visions, different approach — one idea.\n\n"
        "📋 *Details:*\n"
        "• Duration: 30 minutes\n"
        "• Two photographers (my page & Lida’s)\n"
        "• Limited spots available\n"
        "• Price: 150 CAD\n"
        "• The heart of this shoot — a vintage car 🚗\n\n"
        "*Please choose a language / Будь ласка, виберіть мову:*\n"
        "1. Українська 🇺🇦\n"
        "2. English 🇬🇧\n\n"
        "_Відповідайте лише цифрою — 1 або 2_"
    )

    await update.message.reply_text(message, parse_mode='Markdown')
    return LANG

async def lang_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    if text == '1':
        context.user_data['lang'] = 'uk'
    elif text == '2':
        context.user_data['lang'] = 'en'
    else:
        await update.message.reply_text("Будь ласка, виберіть *1* або *2* / Please choose *1* or *2*", parse_mode='Markdown')
        return LANG

    qlist = questions_uk if context.user_data['lang'] == 'uk' else questions_en
    await update.message.reply_text(qlist[0])
    return INSTAGRAM

async def instagram_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['answers']['name'] = update.message.text.strip()
    qlist = questions_uk if context.user_data['lang'] == 'uk' else questions_en
    await update.message.reply_text(qlist[1])
    return AGE

async def age_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['answers']['instagram'] = update.message.text.strip()
    qlist = questions_uk if context.user_data['lang'] == 'uk' else questions_en
    await update.message.reply_text(qlist[2])
    return WHY

async def why_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['answers']['age'] = update.message.text.strip()
    qlist = questions_uk if context.user_data['lang'] == 'uk' else questions_en
    await update.message.reply_text(qlist[3])
    return OUTFIT

async def outfit_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['answers']['why'] = update.message.text.strip()
    qlist = questions_uk if context.user_data['lang'] == 'uk' else questions_en
    await update.message.reply_text(qlist[4])
    return HELP

async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['answers']['outfit'] = update.message.text.strip()
    qlist = questions_uk if context.user_data['lang'] == 'uk' else questions_en
    await update.message.reply_text(qlist[5])
    return WISHES

async def wishes_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['answers']['help'] = update.message.text.strip()
    qlist = questions_uk if context.user_data['lang'] == 'uk' else questions_en
    await update.message.reply_text(qlist[6])
    return PUBLIC

async def public_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['answers']['wishes'] = update.message.text.strip()
    await update.message.reply_text(
        "💡 Якщо є запитання або побажання — напиши їх тут :)\n"
        "✍️ If you have any questions or requests — feel free to write them here :)"
    )
    return QUESTIONS

async def questions_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['answers']['public'] = update.message.text.strip()
    context.user_data['answers']['questions'] = update.message.text.strip()

    answers = context.user_data['answers']
    lang = context.user_data['lang']

    response = "Дякуємо за заповнення анкети! Ось ваші відповіді:\n\n" if lang == 'uk' else "Thank you for filling the form! Here are your answers:\n\n"
    keys_uk = ["Ім'я", "Нік Instagram", "Вік", "Чому цікавить", "Образ/одяг", "Допомога з вибором", "Побажання", "Публічність фото", "Запитання"]
    keys_en = ["Name", "Instagram nick", "Age", "Why interested", "Outfit", "Help needed", "Wishes", "Photo public", "Questions"]
    keys = keys_uk if lang == 'uk' else keys_en

    for k, v in zip(keys, answers.values()):
        response += f"{k}: {v}\n"

    await update.message.reply_text(response)

    # Надсилаємо тобі
    await context.bot.send_message(
        chat_id=MY_CHAT_ID,
        text=f"НОВА АНКЕТА від @{update.message.from_user.username or 'без username'}\n\n{response}"
    )

    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Анкета скасована. / Form canceled.")
    return ConversationHandler.END

def main():
    TOKEN = os.getenv('BOT_TOKEN')  # ✅ Ось правильний рядок!
    if not TOKEN:
        print("❌ BOT_TOKEN не задано! Задай змінну середовища.")
        return

    app = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            LANG: [MessageHandler(filters.TEXT & ~filters.COMMAND, lang_choice)],
            INSTAGRAM: [MessageHandler(filters.TEXT & ~filters.COMMAND, instagram_handler)],
            AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, age_handler)],
            WHY: [MessageHandler(filters.TEXT & ~filters.COMMAND, why_handler)],
            OUTFIT: [MessageHandler(filters.TEXT & ~filters.COMMAND, outfit_handler)],
            HELP: [MessageHandler(filters.TEXT & ~filters.COMMAND, help_handler)],
            WISHES: [MessageHandler(filters.TEXT & ~filters.COMMAND, wishes_handler)],
            PUBLIC: [MessageHandler(filters.TEXT & ~filters.COMMAND, public_handler)],
            QUESTIONS: [MessageHandler(filters.TEXT & ~filters.COMMAND, questions_handler)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    app.add_handler(conv_handler)
    print("✅ Бот запущено!")
    app.run_polling()

if __name__ == '__main__':
    main()
