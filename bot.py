from telegram import Update, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import Application, CommandHandler, ContextTypes, InlineQueryHandler, CallbackQueryHandler, MessageHandler, filters
import json
import os
import base64
import io
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
    audio_data = track.get('audio')
    
    keyboard = [
        [InlineKeyboardButton("🔙 К списку треков", callback_data="my_tracks")],
        [InlineKeyboardButton("🎵 Открыть в редакторе", web_app=WebAppInfo(url=WEBAPP_URL))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Если есть аудио, отправляем его
    if audio_data:
        try:
            audio_bytes = base64.b64decode(audio_data)
            audio_file = io.BytesIO(audio_bytes)
            audio_file.name = f"{track_name}.wav"
            
            await query.message.reply_audio(
                audio=audio_file,
                title=track_name,
                performer="Beat Maker",
                reply_markup=reply_markup
            )
            
            await query.edit_message_text(
                f"🎵 *{track_name}*\n\n"
                f"BPM: {track_data.get('bpm', 120)}\n"
                f"Паттерны: {len(track_data.get('patterns', []))}\n"
                f"Дата создания: {track.get('date', 'Неизвестно')}\n\n"
                f"✅ Аудио отправлено!",
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
        except Exception as e:
            print(f"Error sending audio: {e}")
            await query.edit_message_text(
                f"🎵 *{track_name}*\n\n"
                f"BPM: {track_data.get('bpm', 120)}\n"
                f"Паттерны: {len(track_data.get('patterns', []))}\n"
                f"Дата создания: {track.get('date', 'Неизвестно')}\n\n"
                f"❌ Ошибка при отправке аудио.",
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
    else:
        await query.edit_message_text(
            f"🎵 *{track_name}*\n\n"
            f"BPM: {track_data.get('bpm', 120)}\n"
            f"Паттерны: {len(track_data.get('patterns', []))}\n"
            f"Дата создания: {track.get('date', 'Неизвестно')}\n\n"
            f"⚠️ Аудио не найдено. Экспортируй трек из редактора.",
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

async def handle_webapp_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик данных из WebApp"""
    user_id = update.effective_user.id
    
    # Данные приходят через update.message.text (JSON строка)
    if update.message and update.message.text:
        try:
            track_data = json.loads(update.message.text)
            
            if user_id not in tracks_storage:
                tracks_storage[user_id] = []
            
            # Сохраняем трек
            track = {
                'name': track_data.get('name', f'Трек {len(tracks_storage[user_id]) + 1}'),
                'date': datetime.now().strftime('%d.%m.%Y %H:%M'),
                'data': {
                    'patterns': track_data.get('patterns', []),
                    'bpm': track_data.get('bpm', 120),
                    'steps': track_data.get('steps', 16),
                    'currentPattern': track_data.get('currentPattern', 0)
                },
                'audio': track_data.get('audio')  # Base64 аудио
            }
            
            tracks_storage[user_id].append(track)
            
            keyboard = [
                [InlineKeyboardButton("🎧 Мои треки", callback_data="my_tracks")],
                [InlineKeyboardButton("🎵 Создать ещё", web_app=WebAppInfo(url=WEBAPP_URL))]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.message.reply_text(
                f"✅ *Трек сохранён!*\n\n"
                f"Название: {track['name']}\n"
                f"BPM: {track['data']['bpm']}\n"
                f"Паттерны: {len(track['data']['patterns'])}\n\n"
                f"Используй кнопку 'Мои треки' чтобы прослушать все треки! 🎵",
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
            
            # Если есть аудио, отправляем его сразу
            if track_data.get('audio'):
                try:
                    audio_bytes = base64.b64decode(track_data['audio'])
                    audio_file = io.BytesIO(audio_bytes)
                    audio_file.name = f"{track['name']}.wav"
                    
                    await update.message.reply_audio(
                        audio=audio_file,
                        title=track['name'],
                        performer="Beat Maker"
                    )
                except Exception as e:
                    print(f"Error sending audio: {e}")
                    
        except json.JSONDecodeError:
            await update.message.reply_text("❌ Ошибка при сохранении трека. Попробуйте снова.")
        except Exception as e:
            print(f"Error saving track: {e}")
            await update.message.reply_text("❌ Произошла ошибка. Попробуйте снова.")

def main():
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("mytracks", my_tracks))
    app.add_handler(CallbackQueryHandler(my_tracks, pattern="^my_tracks$"))
    app.add_handler(CallbackQueryHandler(play_track, pattern="^play_track_"))
    app.add_handler(CallbackQueryHandler(back_to_start, pattern="^back_to_start$"))
    
    # Обработчик данных из WebApp (приходят как текстовые сообщения с JSON)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_webapp_data))
    
    print("Bot started!")
    app.run_polling()

if __name__ == '__main__':
    main()
