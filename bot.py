import telebot
from telebot import types
import os

TOKEN = '7292986121:AAEcpsXiKfN7qWXAANwMyrZb7BRB5C1L7DA'
bot = telebot.TeleBot(TOKEN)

# Уроки и табы
lessons = [
    {"video": "урок01-знакомство.mp4"},
    {"video": "урок02-подготовка.mp4"},
    {"video": "урок03-правильная_посадка.mp4"},
    {"video": "урок04-правая_рука.mp4"},
    {"video": "урок05-левая_рука.mp4"},
    {"video": "урок06-Первое произведение.mp4", "tab": "урок06 Smoke on the water.pdf"},
    {"video": "урок07-Миссия невыполнима.mp4", "tab": "урок07 Миссия Невыполнима.pdf"},
    {"video": ["урок08-Читаем табы.mp4", "урок08-Prayer in C.mp4"], "tab": "урок8 Prayer In C.pdf"},
    {"video": "урок09-Чередование пальцев.mp4", "tab": "урок09-Лесник.pdf"},
    {"video": "урок10-навалим баса.mp4", "tab": "урок10-Черный Бумер.pdf"},
    {"video": "урок11-Счет и ритм.mp4", "tab": "урок11-Длительности.pdf"},
    {"video": "урок12-Вырабатываем правильный ритм.mp4", "tab": "урок12-Кукла Колдуна.pdf"},
    {"video": "урок13-Закрепляем пройденное.mp4", "tab": "урок13-Конь - Любэ.pdf"},
    {"video": "урок14-Итоги обучения.mp4"},
    {"video": "урок15-Развитие.mp4"},
]

# Словарь: user_id -> номер текущего урока
user_progress = {}

# Кнопка "Учиться"
def get_learn_keyboard():
    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton("Учиться 🎸", callback_data="learn")
    markup.add(btn)
    return markup

# Старт
@bot.message_handler(commands=['start'])
def start_message(message):
    user_progress[message.chat.id] = 0
    bot.send_message(message.chat.id, "Привет! Нажми кнопку, чтобы начать обучение 🎸", reply_markup=get_learn_keyboard())

# Кнопка "Учиться"
@bot.callback_query_handler(func=lambda call: call.data == "learn")
def send_lesson(call):
    user_id = call.message.chat.id
    step = user_progress.get(user_id, 0)

    if step >= len(lessons):
        bot.send_message(user_id, "🎉 Ты прошёл все уроки! Молодец!")
        return

    lesson = lessons[step]

    videos = lesson["video"]
    if isinstance(videos, str):
        videos = [videos]

    for video in videos:
        path = f"lessons/{video}"
        if os.path.exists(path):
            with open(path, 'rb') as video_file:
                bot.send_video(user_id, video_file, caption=video.replace(".mp4", ""))
        else:
            bot.send_message(user_id, f"Не найден файл: {video}")

    # Табы
    if "tab" in lesson:
        tab_path = f"lessons/{lesson['tab']}"
        if os.path.exists(tab_path):
            with open(tab_path, 'rb') as tab_file:
                bot.send_document(user_id, tab_file)
        else:
            bot.send_message(user_id, f"Не найден таб: {lesson['tab']}")

    user_progress[user_id] = step + 1
    bot.send_message(user_id, "Готов продолжить?", reply_markup=get_learn_keyboard())

# Запуск
bot.polling(none_stop=True)
