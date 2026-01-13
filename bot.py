from telegram import Update, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

# ВСТАВЬ СВОЙ ТОКЕН СЮДА (от BotFather)
TOKEN = "ВСТАВЬ_ТОКЕН_СЮДА"

# Ссылка на твой сайт
WEBAPP_URL = "https://uno555dos777.github.io/bitochek/"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🎵 Открыть Beat Maker", web_app=WebAppInfo(url=WEBAPP_URL))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🎵 *Добро пожаловать в Beat Maker!*\n\n"
        "Создавай профессиональные биты прямо в Telegram!\n\n"
        "Нажми кнопку ниже чтобы начать 👇",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    
    print("🤖 Бот запущен!")
    app.run_polling()

if __name__ == '__main__':
    main()

