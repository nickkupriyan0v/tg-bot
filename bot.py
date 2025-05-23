import telebot
import os
from all_cities import get_all_cities
import random

cities_list = get_all_cities()
cities = {city.lower(): city for city in cities_list}


TOKEN = os.getenv('TELEGRAM_TOKEN')

bot = telebot.TeleBot(TOKEN)
games = {}


def get_last_letter(city):
    city_lower = city.lower()
    last_char = city_lower[-1]
    if last_char in ['ь', 'ы', 'й', 'ъ']:
        return city_lower[-2]
    else:
        return last_char


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(
        message, "Привет! Это бот для игры в города. Начни игру командой /start_game")


@bot.message_handler(commands=['start_game'])
def start_game(message):
    user_id = message.chat.id
    games.pop(user_id, None)  # Сброс предыдущей игры

    if not cities_list:
        bot.send_message(user_id, "Ошибка: список городов пуст.")
        return

    starting_city = random.choice(cities_list)
    games[user_id] = {
        'used': [starting_city.lower()],
        'last_city': starting_city
    }
    next_letter = get_last_letter(starting_city)
    bot.send_message(
        user_id, f"Игра началась! Первый город: {starting_city.capitalize()}\nВаш ход. Назовите город на букву '{next_letter.upper()}'")


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.chat.id
    if user_id not in games:
        bot.send_message(user_id, "Начните игру командой /start_game")
        return

    user_input = message.text.strip()
    user_city_lower = user_input.lower()
    game_data = games[user_id]

    # Проверка существования города
    if user_city_lower not in cities:
        bot.send_message(user_id, "Такого города нет в моём списке.")
        return

    # Проверка на повтор
    if user_city_lower in game_data['used']:
        bot.send_message(user_id, "Этот город уже был использован.")
        return

    # Проверка начальной буквы
    required_letter = get_last_letter(game_data['last_city'])
    if user_city_lower[0] != required_letter:
        bot.send_message(
            user_id, f"Город должен начинаться на букву '{required_letter.upper()}'")
        return

    # Добавляем город пользователя
    game_data['used'].append(user_city_lower)
    # Получаем оригинальное написание
    original_city_name = cities[user_city_lower]
    game_data['last_city'] = original_city_name

    # Определяем следующую букву для бота
    next_letter = get_last_letter(user_city_lower)

    # Поиск доступных городов
    available = [
        city for city in cities.values()
        if city.lower() not in game_data['used'] and city.lower().startswith(next_letter)
    ]

    if not available:
        bot.send_message(
            user_id, "Я не могу найти подходящий город. Вы победили!")
        del games[user_id]
    else:
        bot_city = random.choice(available)
        bot_city_lower = bot_city.lower()
        game_data['used'].append(bot_city_lower)
        game_data['last_city'] = bot_city
        next_letter_user = get_last_letter(bot_city_lower)
        bot.send_message(
            user_id, f"Мой город: {bot_city.capitalize()}\nВаш ход! Назовите город на букву '{next_letter_user.upper()}'")


if __name__ == '__main__':
    bot.polling()
