import telebot
import os
import random

# Конфигурация
TOKEN = '8066421541:AAHmSuQUj-1j1ImVgadJA7L5HYXbgN7rn2o'
AUTHOR_IMAGE_PATH = 'images/author.jpg'
TEXTS_FOLDER = 'texts/'
IMAGES_FOLDER = 'images/'

bot = telebot.TeleBot(TOKEN)

# Загрузка текстов в память
texts = {}
for filename in os.listdir(TEXTS_FOLDER):
    if filename.endswith('.txt'):
        with open(os.path.join(TEXTS_FOLDER, filename), 'r', encoding='windows-1251') as f:
            texts[filename[:-4]] = f.read()

# Главное меню
main_menu = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
main_menu.add('О чат-боте', 'Поиск произведения по названию', 'Поиск произведения по словам')

@bot.message_handler(commands=['start', 'run', 'activate'])
def start_bot(message):
    bot.send_message(
        message.chat.id,
        "Добро пожаловать! Этот бот служит для поиска произведений выбранного писателя.",
        reply_markup=main_menu
    )

@bot.message_handler(func=lambda message: message.text == 'О чат-боте')
def about_bot(message):
    bot.send_message(
        message.chat.id,
        "Этот бот разработан студентом Рязановым Тимофеем из группы 8И42 и служит для поиска произведений выбранного писателя."
    )
    bot.send_message(message.chat.id, "Выберите действие:", reply_markup=main_menu)

@bot.message_handler(func=lambda message: message.text == 'Поиск произведения по названию')
def search_by_title(message):
    bot.send_message(message.chat.id, "Введите название произведения:")
    bot.register_next_step_handler(message, find_title)

def find_title(message):
    title = message.text
    if title.lower() in " ".join(texts.keys()).lower():
        for t in texts:
            if title.lower() in t.lower():
                text = t
        fragment = text[:200] + '...'  # Первые 200 символов
        image_path = os.path.join(IMAGES_FOLDER, f"{title}.jpg")
        if os.path.exists(image_path):
            with open(image_path, 'rb') as img:
                bot.send_photo(message.chat.id, img, caption=fragment)
        else:
            with open(AUTHOR_IMAGE_PATH, 'rb') as img:
                bot.send_photo(message.chat.id, img, caption=fragment)
    else:
        bot.send_message(message.chat.id, "Произведение не найдено.")
    bot.send_message(message.chat.id, "Выберите действие:", reply_markup=main_menu)

@bot.message_handler(func=lambda message: message.text == 'Поиск произведения по словам')
def search_by_words(message):
    bot.send_message(message.chat.id, "Введите слово для поиска:")
    bot.register_next_step_handler(message, find_words)

def find_words(message):
    word = message.text.lower()
    found_titles = [title for title, text in texts.items() if word in text.lower()]
    if found_titles:
        bot.send_message(
            message.chat.id,
            "Слово найдено в следующих произведениях:\n" + '\n'.join(found_titles)
        )
    else:
        bot.send_message(message.chat.id, "Слово не найдено ни в одном произведении.")
    bot.send_message(message.chat.id, "Выберите действие:", reply_markup=main_menu)

if __name__ == '__main__':
    print("Бот запущен...")
    bot.polling(none_stop=True)
