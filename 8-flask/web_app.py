"""
Написать веб-приложение на Flask со следующими ендпоинтами:
    - главная страница - содержит ссылки на все остальные страницы
    - /duck/ - отображает заголовок "рандомная утка №ххх" и картинка утки
                которую получает по API https://random-d.uk/

    - /fox/<int>/ - аналогично утке только с лисой (- https://randomfox.ca),
                    но количество разных картинок определено int.
                    если int больше 10 или меньше 1 - вывести сообщение
                    что можно только от 1 до 10

    - Добавить обработчик ошибки 404


(8) Повторить проект с приложением QUIZ (папка flask3)
  Добавить возможность                     / Написать приложение-галерею
  (оригинальное задание):                  /  со следующими возможностями:
    - просматривать все квизы и вопросы    / - просматривать все картины галерее и подписи
    - добавлять квизы и вопросы            / - добавлять картины, (имя файла, название, дата строкой, размеры, материал или техника,
                                                                                         цена, в наличии, продано)
    - редактировать квизы и вопросы        / - редактировать картины, цены и поля описания
    - удалять квизы и вопросы              / - удалять галереи и записи о картинах
    - изменять связи вопросов с квизами    / - изменять связи картин с галереями

  Добавить оформление через стили CSS на свое усмотрение

"""

from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_wtf.csrf import CSRFProtect

import os

from duck_fox import get_random_duck_and_its_number, get_foxy_urls
from models import db, User, Painting, Gallery, db_add_new_data
from api_calls import *
from forms import FormAddGallery, FormAddPaintings, FormAddUser


# BASE_DIR = os.path.dirname(__name__)  # так работает если проект открыт из любого места
BASE_DIR = os.path.dirname(__file__)  # получаем тут абсолютный путь
DB_PATH = os.path.join(BASE_DIR, "db", "gallery.db")

MAX_FOX_CNT = 124  # максимальное количество лисиц на randomfox.ca


html_config = {"admin": True, "debug": False}

app = Flask(
    __name__,
    static_folder=os.path.join(BASE_DIR, "static"),
    template_folder=os.path.join(BASE_DIR, "templates"),
)

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_PATH}"
# Задайте секретный ключ для сессий
# app.config["SECRET_KEY"] = "hastalavistaAbrakadabra336684916"
app.config["SECRET_KEY"] = "secretkeysecretkeysecretkey1212121"
# app.secret_key = 'your_secret_key'
csrf = CSRFProtect(app)  # Инициализация CSRF-защиты форм


# инициализируем Алхимию для веб-приложения
db.init_app(app)
with app.app_context():
    db_add_new_data()


##########
# ROUTES #
##########


@app.route("/")
def index():
    return render_template("default_page.html", html_config=html_config)


@app.route("/duck/")
def duck():
    (img_url, number) = get_random_duck_and_its_number()
    return render_template(
        "duck.html",
        title=f"рандомная утка №{number}",
        img_url=img_url,
        number=number,
        html_config=html_config,
    )


@app.route("/fox/<int:num>/")
def fox(num):
    """Get a random fox image URL from the API"""
    if num < 1 or num > 10:
        return "число должно быть от 1 до 10"

    foxes = get_foxy_urls(num, MAX_FOX_CNT)
    return render_template(
        "fox.html",
        title=f"Pандомная лиса, {num} штук",
        foxes=foxes,
        number=num,
        html_config=html_config,
    )


@app.route("/select-gallery/", methods=["POST", "GET"])
def view_gallery():
    if request.method == "GET":
        session["gallery_id"] = -1
        galleries = Gallery.query.all()
        # print(galleries)
        return render_template(
            "gallery_select.html", galleries=galleries, html_config=html_config
        )
    session["gallery_id"] = request.form.get("gallery")
    session["painting_n"] = 0
    session["question_id"] = 0
    session["right_answers"] = 0
    return redirect(url_for("painting"))


@app.route("/painting/", methods=["POST", "GET"])
def view_painting():

    # если квиз еще не выбран - перенаправляем на выбор
    if not session["gallery_id"] or session["gallery_id"] == -1:
        return redirect(url_for("view_gallery"))

    # если пост значит пришел ответ на вопрос
    if request.method == "POST":
        painting = Painting.query.filter_by(id=session["question_id"]).one()
        # если ответы сходятся значит +1
        if painting.answer == request.form.get("ans_text"):
            session["right_answers"] += 1
        # следующий вопрос
        session["painting_n"] += 1

    gallery = Gallery.query.filter_by(id=session["gallery_id"]).one()

    # если вопросы закончились
    if int(session["painting_n"]) >= len(gallery.painting):
        session["gallery_id"] = -1  # чтобы больше не работала страница question
        return redirect(url_for("view_result"))

    # если вопросы еще не закончились
    else:
        painting = gallery.painting[session["painting_n"]]
        session["question_id"] = painting.id
        answers = [painting.answer, painting.wrong1, painting.wrong2, painting.wrong3]
        # shuffle(answers)

        return render_template(
            "painting.html",
            answers=answers,
            question=painting,
            html_config=html_config,
            image=url_for("static", filename=f"pic-art/{answers[0]}"),
            desc=answers[1],
        )


@app.route("/result/")
def view_result():
    return render_template(
        "result.html",
        right=session["right_answers"],
        total=session["painting_n"],
        html_config=html_config,
        url=url_for("view_gallery"),
    )


### edit pages (adm part) ###


@app.route("/edit/", methods=["POST", "GET"])
def edit():
    gallery_id = request.args.get("gallery_id")

    galleries = api_get_all_galleries()

    # если галерея выбрана, отображаем картины только этой галереи
    if gallery_id:
        gallery_id = int(gallery_id)
    else:
        gallery_id = -1

    # если пост значит добавлена галерея
    if request.method == "POST":
        # получаем данные из формы
        gallery_name = request.form.get("name")
        gallery_user_id = request.form.get("user_id")
        gallery_desc = request.form.get("desc")
        # добавляем галерею в БД
        api_add_gallery(gallery_name, gallery_user_id, gallery_desc)
        return redirect(url_for("edit"), code=302)

    if gallery_id != -1:
        # получить картины для выбранной галереи через API
        pictures = api_get_paintings_by_gallery_id(gallery_id)
        selected_gallery = api_get_gallery(gallery_id)
    else:
        pictures = api_get_all_paintings()
        selected_gallery = None

    return render_template(
        "edit.html",
        galleries=galleries,
        selected_gallery=selected_gallery,
        pictures=pictures,
    )


@app.route("/edit2/", methods=["GET", "POST"])
def edit2():
    gallery_id = request.args.get("gallery_id")

    galleries = api_get_all_galleries()

    # если галерея выбрана, отображаем картины только этой галереи
    if gallery_id:
        gallery_id = int(gallery_id)
    else:
        gallery_id = -1

    if gallery_id != -1:
        # получить картины для выбранной галереи через API
        pictures = api_get_paintings_by_gallery_id(gallery_id)
        selected_gallery = api_get_gallery(gallery_id)
    else:
        pictures = api_get_all_paintings()
        selected_gallery = None

    # # если пост значит добавлена галерея
    # if request.method == "POST":
    #     # получаем данные из формы
    #     gallery_name = request.form.get("name")
    #     gallery_user_id = request.form.get("user_id")
    #     gallery_desc = request.form.get("desc")
    #     # добавляем галерею в БД
    #     api_add_gallery(gallery_name, gallery_user_id, gallery_desc)
    #     return redirect(url_for("edit"), code=302)
    form_add_gal = FormAddGallery()
    if form_add_gal.validate_on_submit():
        name = form_add_gal.name.data
        flash(f"Hello, {name}!")
        return redirect(url_for("edit2"))

    return render_template(
        "edit2.html",
        galleries=galleries,
        selected_gallery=selected_gallery,
        pictures=pictures,
        form_add_gal=form_add_gal,
    )


@app.route("/gallery_delete/<int:gallery_id>", methods=["GET"])
def gallery_delete(gallery_id):
    # Логика удаления галереи по gallery_id
    if request.method == "GET":
        if gallery_id:
            api_delete_gallery(gallery_id)
            # return redirect(url_for("edit"))
            return render_template(
                "edit.html",
                galleries=api_get_all_galleries(),
                selected_gallery=-1,
                pictures=api_get_all_paintings(),
            )
    return "", 204  # OK, No Content


### test pages ###


@app.route("/page1/")
def page1():
    return render_template(
        "page1.html",
        html_config=html_config,
    )


@app.route("/page2/")
def page2():
    return render_template(
        "page2.html",
        html_config=html_config,
    )


# Сработает если ошибка 404 - т.е. любой другой путь который выше не предусмотрен
@app.errorhandler(404)
def page_not_found(error):
    # TODO *** переделать на темплейт
    return '<h1 style="color:red">такой страницы не существует</h1>'


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
