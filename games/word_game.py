from config import bot
from telebot import types
import random
from utils import create_menu

words_list = ['яблоко', 'банан', 'апельсин', 'виноград', 'мандарин']


def start_guess_word(message, user_states, current_word):
    user_id = message.from_user.id
    user_states[user_id] = 'playing_guess_word'
    current_word[user_id] = random.choice(words_list)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton('Выход'))
    bot.send_message(
        message.chat.id, "Угадай загаданное слово. Введи свой вариант:", reply_markup=markup)


def handle_guess(message, user_states, current_word):
    user_id = message.from_user.id
    if message.text == 'Выход':
        user_states.pop(user_id, None)
        current_word.pop(user_id, None)
        bot.send_message(
            message.chat.id, "Игра завершена. Возвращаюсь в меню.", reply_markup=create_menu())
        return

    guess = message.text.strip().lower()
    if guess == current_word.get(user_id, ''):
        bot.send_message(message.chat.id, "✅ Правильно! Ты угадал!")
        user_states.pop(user_id, None)
        current_word.pop(user_id, None)
        bot.send_message(message.chat.id, "Возвращаюсь в меню.",
                         reply_markup=create_menu())
    else:
        bot.send_message(message.chat.id, "❌ Неверно. Попробуй еще раз.")
