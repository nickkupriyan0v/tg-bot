def get_all_cities() -> list[str]:
    cities = []
    with open('cities.txt', 'r', encoding='utf-8') as file:
        cities = [line.strip().lower() for line in file if line.strip()]
    return cities
