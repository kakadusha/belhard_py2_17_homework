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

from flask import Flask, render_template, redirect, url_for, request, session
import os

from duck_fox import get_random_duck_and_its_number, get_foxy_urls
from models import db, User, Painting, Gallery, db_add_new_data

# from models import db, User, Painting, Gallery, db_add_new_data


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
# app.config["SECRET_KEY"] = "hastalavistaAbrakadabra336684916"
app.config["SECRET_KEY"] = "secretkeysecretkeysecretkey1212121"

# инициализируем Алхимию для веб-приложения
db.init_app(app)
with app.app_context():
    db_add_new_data()

##########
# ROUTES #
##########


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


@app.route("/select-gallery/", methods=["POST", "GET"])
def view_gallery():
    if request.method == "GET":
        session["gallery_id"] = -1
        quizes = Gallery.query.all()
        # print(quizes)
        return render_template(
            "gallery_select.html", quizes=quizes, html_config=html_config
        )
    session["gallery_id"] = request.form.get("gallery")
    session["painting_n"] = 0
    session["question_id"] = 0
    session["right_answers"] = 0
    return redirect(url_for("view_painting"))


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
    if request.method == "POST":
        gallery = request.form.get("gallery")
        if gallery and len(gallery) > 3:
            user = User.query.all()
            gallery = Gallery(gallery, user[0])
            db.session.add(gallery)
            db.session.commit()
        else:
            painting = request.form.get("painting") or ""
            answer = request.form.get("answer")
            wrong1 = request.form.get("wrong1")
            wrong2 = request.form.get("wrong2")
            wrong3 = request.form.get("wrong3")
            if all([painting, answer, wrong1, wrong2, wrong3]):
                q = Painting(painting, answer, wrong1, wrong2, wrong3)
                db.session.add(q)
                db.session.commit()

        return redirect(url_for("view_quiz_edit", qqq="123"))

    galleries = Gallery.query.all()
    paintings = Painting.query.all()
    return render_template(
        "edit.html",
        html_config=html_config,
        galleries=galleries,
        paintings=paintings,
        len=len,
    )


### test pages ###


@app.route("/page1/")
def page1():
    return render_template("page1.html")


@app.route("/page2/")
def page2():
    return render_template("page2.html")


# Сработает если ошибка 404 - т.е. любой другой путь который выше не предусмотрен
@app.errorhandler(404)
def page_not_found(error):
    # TODO *** переделать на темплейт
    return '<h1 style="color:red">такой страницы не существует</h1>'


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
