from config import bot
from telebot import types
from games.rps_game import start_rps, handle_rps_choice
from games.cities_game import start_cities, handle_city
from games.word_game import start_guess_word, handle_guess
from utils import create_menu

# Глобальные состояния
user_states = {}
used_cities = {}
last_letter = {}
current_word = {}


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(
        message.chat.id, "Привет! Выбери игру из меню:", reply_markup=create_menu())


@bot.message_handler(func=lambda message: message.text == '❓ Помощь')
def send_help(message):
    help_text = """
Правила игр:
1. 🎮 Камень-ножницы-бумага: выбери один из вариантов.
2. 🏙️ Города: называй города на последнюю букву предыдущего города.
3. 🔤 Угадай слово: отгадай загаданное слово (фрукты).
"""
    bot.send_message(message.chat.id, help_text)


@bot.message_handler(func=lambda message: True)
def main_handler(message):
    user_id = message.from_user.id
    state = user_states.get(user_id)

    if state == 'playing_rps':
        handle_rps_choice(message, user_states)
    elif state == 'playing_cities':
        handle_city(message, user_states, used_cities, last_letter)
    elif state == 'playing_guess_word':
        handle_guess(message, user_states, current_word)
    else:
        if message.text == '🎮 Камень-ножницы-бумага':
            start_rps(message, user_states)
        elif message.text == '🏙️ Города':
            start_cities(message, user_states, used_cities, last_letter)
        elif message.text == '🔤 Угадай слово':
            start_guess_word(message, user_states, current_word)
        else:
            bot.send_message(
                message.chat.id, "Выбери игру из меню:", reply_markup=create_menu())


if __name__ == '__main__':
    bot.polling(none_stop=True)
