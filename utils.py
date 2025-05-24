from telebot import types
from pathlib import Path


def create_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton('🎮 Камень-ножницы-бумага'))
    markup.add(types.KeyboardButton('🏙️ Города'))
    markup.add(types.KeyboardButton('🔤 Угадай слово'))
    markup.add(types.KeyboardButton('❓ Помощь'))
    return markup


def get_all_cities() -> list[str]:
    cities = []
    script_dir = Path(__file__).parent  # Директория скрипта
    file_path = script_dir / 'cities.txt'
    with open(file_path, 'r', encoding='utf-8') as file:
        cities = [line.strip() for line in file if line.strip()]
    return cities
