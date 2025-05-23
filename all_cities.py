from pathlib import Path

def get_all_cities() -> list[str]:
    cities = []
    script_dir = Path(__file__).parent  # Директория скрипта
    file_path = script_dir / 'cities.txt'
    with open(file_path, 'r', encoding='utf-8') as file:
        cities = [line.strip().lower() for line in file if line.strip()]
    return cities
