from config import bot
from telebot import types
from utils import create_menu, get_all_cities

cities_list = get_all_cities()


def start_cities(message, user_states, used_cities, last_letter):
    user_id = message.from_user.id
    user_states[user_id] = 'playing_cities'
    used_cities[user_id] = []
    last_letter[user_id] = None
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton('Выход'))
    bot.send_message(
        message.chat.id, "Назови город. Первый город называешь ты:", reply_markup=markup)


def handle_city(message, user_states, used_cities, last_letter):
    user_id = message.from_user.id
    if message.text == 'Выход':
        user_states.pop(user_id, None)
        used_cities.pop(user_id, None)
        last_letter.pop(user_id, None)
        bot.send_message(
            message.chat.id, "Игра завершена. Возвращаюсь в меню.", reply_markup=create_menu())
        return

    city = message.text.strip().capitalize()

    if city not in cities_list:
        bot.send_message(
            message.chat.id, "Такого города нет в списке. Попробуй еще.")
        return
    if city in used_cities.get(user_id, []):
        bot.send_message(message.chat.id, "Этот город уже был. Назови другой.")
        return

    if last_letter.get(user_id):
        if city[0].lower() != last_letter[user_id].lower():
            bot.send_message(
                message.chat.id, f"Город должен начинаться на '{last_letter[user_id]}'. Попробуй еще.")
            return

    used_cities[user_id].append(city)
    last_char = city[-1].lower()
    if last_char in ['ь', 'ы', 'й', 'ъ']:
        last_char = city[-2].lower()
    last_letter[user_id] = last_char

    bot_city = next((c for c in cities_list
                    if c not in used_cities[user_id] and c[0].lower() == last_char), None)

    if not bot_city:
        bot.send_message(
            message.chat.id, "Ты выиграл! Я не знаю больше городов.")
        user_states.pop(user_id, None)
        used_cities.pop(user_id, None)
        last_letter.pop(user_id, None)
        bot.send_message(message.chat.id, "Возвращаюсь в меню.",
                         reply_markup=create_menu())
        return

    used_cities[user_id].append(bot_city)
    last_char_bot = bot_city[-1].lower()
    if last_char_bot in ['ь', 'ы', 'й', 'ъ']:
        last_char_bot = bot_city[-2].lower()
    last_letter[user_id] = last_char_bot

    bot.send_message(
        message.chat.id, f"Мой город: {bot_city}. Тебе на букву '{last_char_bot.upper()}'. Назови город:")
