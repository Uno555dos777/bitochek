from telegram import Update, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import Application, CommandHandler, ContextTypes, InlineQueryHandler, CallbackQueryHandler
import json
import os
from datetime import datetime

# ВСТАВЬ СВОЙ ТОКЕН СЮДА (от BotFather)
TOKEN = "8445445371:AAEbsxGBm61REb_9ycdZX7aTVgJZfRjN8ec"

# Ссылка на твой сайт
WEBAPP_URL = "https://uno555dos777.github.io/bitochek/"

# Хранилище треков (в реальном проекте используй БД)
tracks_storage = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🎵 Открыть Beat Maker", web_app=WebAppInfo(url=WEBAPP_URL))],
        [InlineKeyboardButton("🎧 Мои треки", callback_data="my_tracks")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🎵 *Добро пожаловать в Beat Maker!*\n\n"
        "Создавай профессиональные биты прямо в Telegram!\n\n"
        "Нажми кнопку ниже чтобы начать 👇",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def my_tracks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    
    # Получаем треки пользователя
    user_tracks = tracks_storage.get(user_id, [])
    
    if not user_tracks:
        keyboard = [
            [InlineKeyboardButton("🎵 Создать трек", web_app=WebAppInfo(url=WEBAPP_URL)),
             InlineKeyboardButton("🔙 Назад", callback_data="back_to_start")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            "🎧 *Мои треки*\n\n"
            "У тебя пока нет сохранённых треков.\n\n"
            "Создай свой первый бит! 🎵",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
        return
    
    # Формируем список треков
    keyboard = []
    for i, track in enumerate(user_tracks[:10]):  # Показываем первые 10
        track_name = track.get('name', f'Трек {i+1}')
        track_date = track.get('date', 'Неизвестно')
        keyboard.append([InlineKeyboardButton(
            f"🎵 {track_name} ({track_date})",
            callback_data=f"play_track_{i}"
        )])
    
    keyboard.append([InlineKeyboardButton("🔙 Назад", callback_data="back_to_start")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        f"🎧 *Мои треки*\n\n"
        f"Найдено треков: {len(user_tracks)}\n\n"
        f"Выбери трек для прослушивания:",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def play_track(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    track_index = int(query.data.split('_')[-1])
    user_id = query.from_user.id
    
    user_tracks = tracks_storage.get(user_id, [])
    
    if track_index >= len(user_tracks):
        await query.answer("Трек не найден", show_alert=True)
        return
    
    track = user_tracks[track_index]
    track_name = track.get('name', f'Трек {track_index+1}')
    track_data = track.get('data', {})
    
    # Здесь должна быть логика воспроизведения трека
    # Пока просто показываем информацию
    keyboard = [
        [InlineKeyboardButton("🔙 К списку треков", callback_data="my_tracks")],
        [InlineKeyboardButton("🎵 Открыть в редакторе", web_app=WebAppInfo(url=WEBAPP_URL))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        f"🎵 *{track_name}*\n\n"
        f"BPM: {track_data.get('bpm', 120)}\n"
        f"Паттерны: {len(track_data.get('patterns', []))}\n"
        f"Дата создания: {track.get('date', 'Неизвестно')}\n\n"
        f"⚠️ Воспроизведение треков будет добавлено в следующем обновлении.",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def back_to_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [InlineKeyboardButton("🎵 Открыть Beat Maker", web_app=WebAppInfo(url=WEBAPP_URL))],
        [InlineKeyboardButton("🎧 Мои треки", callback_data="my_tracks")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        "🎵 *Добро пожаловать в Beat Maker!*\n\n"
        "Создавай профессиональные биты прямо в Telegram!\n\n"
        "Нажми кнопку ниже чтобы начать 👇",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def save_track(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик сохранения трека из WebApp"""
    # WebApp отправляет данные через callback_data или через сообщение
    # Здесь нужно обработать сохранение трека
    user_id = update.effective_user.id
    
    if user_id not in tracks_storage:
        tracks_storage[user_id] = []
    
    # В реальном проекте здесь будет парсинг данных из WebApp
    # Пока заглушка
    track_data = {
        'name': f'Трек {len(tracks_storage[user_id]) + 1}',
        'date': datetime.now().strftime('%d.%m.%Y'),
        'data': {}
    }
    
    tracks_storage[user_id].append(track_data)
    
    await update.message.reply_text(
        f"✅ Трек сохранён!\n\n"
        f"Используй /mytracks чтобы посмотреть все треки."
    )

def main():
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("mytracks", my_tracks))
    app.add_handler(CallbackQueryHandler(my_tracks, pattern="^my_tracks$"))
    app.add_handler(CallbackQueryHandler(play_track, pattern="^play_track_"))
    app.add_handler(CallbackQueryHandler(back_to_start, pattern="^back_to_start$"))
    
    print("Bot started!")
    app.run_polling()

if __name__ == '__main__':
    main()
