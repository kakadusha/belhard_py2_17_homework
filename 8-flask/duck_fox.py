"""
Модуль для функций страницек ducks и foxes
"""

import requests
import random


def get_random_duck_and_its_number() -> tuple:
    """Get a random duck image URL from the API
    returns(url, number)
    """
    url = "https://random-d.uk/api/v2/random"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        num = data["url"].split("/")[-1].split(".")[0]
        return data["url"], num
    else:
        return None, None


def get_foxy_urls(count: int, max: int) -> list:
    """Генерирует список случайных лисиц из randomfox.ca
    в цикле count выбрасывает случайное число от 1 и до max"""
    foxes = []
    for i in range(count):
        num = random.randint(1, max)
        foxes.append(f"https://randomfox.ca/images/{num}.jpg")
    return foxes
