from config import bot
from telebot import types
import random
from utils import create_menu


def start_rps(message, user_states):
    user_id = message.from_user.id
    user_states[user_id] = 'playing_rps'
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton('Камень'), types.KeyboardButton(
        'Ножницы'), types.KeyboardButton('Бумага'))
    markup.add(types.KeyboardButton('Выход'))
    bot.send_message(
        message.chat.id, "Выбери: Камень, Ножницы или Бумага:", reply_markup=markup)


def handle_rps_choice(message, user_states):
    user_id = message.from_user.id
    if message.text == 'Выход':
        user_states.pop(user_id, None)
        bot.send_message(message.chat.id, "Возвращаюсь в меню.",
                         reply_markup=create_menu())
        return

    choices = ['Камень', 'Ножницы', 'Бумага']
    bot_choice = random.choice(choices)
    user_choice = message.text

    if user_choice not in choices:
        bot.send_message(
            message.chat.id, "Пожалуйста, выбери вариант из предложенных.")
        return

    # Определение победителя
    if user_choice == bot_choice:
        result = "Ничья!"
    elif (user_choice == 'Камень' and bot_choice == 'Ножницы') or \
         (user_choice == 'Ножницы' and bot_choice == 'Бумага') or \
         (user_choice == 'Бумага' and bot_choice == 'Камень'):
        result = "Ты выиграл!"
    else:
        result = "Бот выиграл!"

    bot.send_message(message.chat.id,
                     f"Твой выбор: {user_choice}\nВыбор бота: {bot_choice}\nРезультат: {result}")
    start_rps(message, user_states)
