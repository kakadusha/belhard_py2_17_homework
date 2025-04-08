"""
Написать веб-приложение на Flask со следующими ендпоинтами:
    - главная страница - содержит ссылки на все остальные страницы
    - /duck/ - отображает заголовок "рандомная утка №ххх" и картинка утки
                которую получает по API https://random-d.uk/

    - /fox/<int>/ - аналогично утке только с лисой (- https://randomfox.ca),
                    но количество разных картинок определено int.
                    если int больше 10 или меньше 1 - вывести сообщение
                    что можно только от 1 до 10

    *** TBD ***

    - /weather-minsk/ - показывает погоду в минске в красивом формате

    - /weather/<city>/ - показывает погоду в городе указанного в city

    - по желанию добавить еще один ендпоинт на любую тему


Добавить обработчик ошибки 404. (есть в example)
"""

from flask import Flask, render_template
import os
import requests
import random

BASE_DIR = os.path.dirname(__name__)  # так работает если проект открыт из любого места
MAX_FOX_CNT = 124  # максимальное количество лисиц на randomfox.ca

app = Flask(
    __name__,
    static_folder=os.path.join(BASE_DIR, "static"),
    template_folder=os.path.join(BASE_DIR, "templates"),
)


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


@app.route("/")
def index():
    return render_template("default_page.html")


@app.route("/duck/")
def duck():
    (img_url, number) = get_random_duck_and_its_number()
    return render_template(
        "duck.html", title=f"рандомная утка №{number}", img_url=img_url, number=number
    )


@app.route("/fox/<int:num>/")
def fox(num):
    """Get a random fox image URL from the API"""
    if num < 1 or num > 10:
        return "число должно быть от 1 до 10"

    foxes = get_foxy_urls(num, MAX_FOX_CNT)
    return render_template(
        "fox.html", title=f"Pандомная лиса, {num} штук", foxes=foxes, number=num
    )


@app.route("/page1/")
def home():
    return render_template("page1.html")


@app.route("/page2/")
def page2():
    return render_template("page2.html")


# Сработает если ошибка 404 - т.е. любой другой путь который выше не предусмотрен
@app.errorhandler(404)
def page_not_found(error):
    return '<h1 style="color:red">такой страницы не существует</h1>'


if __name__ == "__main__":
    app.run(debug=True)
