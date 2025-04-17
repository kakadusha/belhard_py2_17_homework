# pip install flask_sqlalhemy

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    # __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25))
    quizes = db.relationship(
        "Galery", backref="user", cascade="all, delete, delete-orphan"
    )

    def __init__(self, name) -> None:
        super().__init__()
        self.name = name

    def __repr__(self):
        return f"{self.name}"


# many_to_many
galery_painting = db.Table(
    "galery_painting",
    db.Column("quiz_id", db.Integer, db.ForeignKey("galery.id"), primary_key=True),
    db.Column(
        "question_id", db.Integer, db.ForeignKey("painting.id"), primary_key=True
    ),
)


class Galery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    painting = []

    def __init__(self, name: str, user: User) -> None:
        super().__init__()
        self.name = name
        self.user = user

    def __repr__(self) -> str:
        return f"id - {self.id}, name - {self.name} #"


class Painting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(250), nullable=False)
    answer = db.Column(db.String(100), nullable=False)
    wrong1 = db.Column(db.String(100), nullable=False)
    wrong2 = db.Column(db.String(100), nullable=False)
    wrong3 = db.Column(db.String(100), nullable=False)
    # Эта строка устанавливает двустороннюю связь между Painting и Galery. Вы можете получить список тестов, связанных с вопросом, через question_instance.quiz, и список вопросов, связанных с тестом, через quiz_instance.question.  backref делает код более чистым и удобным в использовании, избегая сложных запросов к базе данных
    galery = db.relationship("Galery", secondary=galery_painting, backref="painting")

    def __init__(self, question: str, answer, wrong1, wrong2, wrong3) -> None:
        super().__init__()
        self.question = question
        self.answer = answer
        self.wrong1 = wrong1
        self.wrong2 = wrong2
        self.wrong3 = wrong3

    def __repr__(self):
        return f"{self.id}-{self.question}"


def db_add_new_data():
    db.drop_all()
    db.create_all()

    user1 = User(name="User1")
    user2 = User(name="User2")

    gals = [
        Galery("Небо", user1),
        Galery("Птицы", user1),
        Galery("Цветы", user2),
        Galery("Миниатюры", user2),
        Galery("Животные", user2),
        Galery("Другое", user2),
    ]

    paintings = [
        Painting(
            "Фиолетовый вечер",
            "IMG_2050.JPG",
            "90x60, Холст, Масло, 2023",
            "lotus",
            "iste",
        ),
        Painting(
            "Уезжать и возвращаться",
            "IMG_2116.JPEG",
            "ipsum",
            "lotus",
            "iste",
        ),
        Painting(
            "Take Me Home, 30x40, Холст, Масло, 2024",
            "IMG_3685.JPEG",
            "90х60, Холст, Масло, 2024",
            "lotus",
            "iste",
        ),
        Painting(
            "El Prat. На рассвете",
            "IMG_6459.JPEG",
            "35x50, Холст, Масло, 2024",
            "lotus",
            "iste",
        ),
        Painting(
            "Раннее утро",
            "IMG_6459.JPEG",
            "80х60, Холст, Масло, 2024",
            "lotus",
            "iste",
        ),
        Painting(
            "В путь",
            "IMG_6539.JPEG",
            "80х60, Холст, Масло, 2023",
            "lotus",
            "iste",
        ),
        Painting(
            "Облачная сиеста 2",
            "IMG_6662.JPG",
            "Холст, Масло, 30х20, 2024",
            "lotus",
            "iste",
        ),
    ]

    # IMG_9987.JPEG

    gals[0].painting.append(paintings[0])
    gals[0].painting.append(paintings[1])
    gals[0].painting.append(paintings[2])

    gals[1].painting.append(paintings[3])
    gals[1].painting.append(paintings[4])
    gals[1].painting.append(paintings[5])
    gals[1].painting.append(paintings[6])
    gals[1].painting.append(paintings[0])

    gals[2].painting.append(paintings[6])
    gals[2].painting.append(paintings[5])
    gals[2].painting.append(paintings[4])

    gals[3].painting.append(paintings[6])
    gals[3].painting.append(paintings[0])
    gals[3].painting.append(paintings[1])
    gals[3].painting.append(paintings[3])

    gals[4].painting.append(paintings[6])
    gals[4].painting.append(paintings[0])
    gals[4].painting.append(paintings[1])
    gals[4].painting.append(paintings[3])

    # db.session.add(quiz)
    db.session.add_all(gals)
    db.session.commit()


"""
УПРАВЛЕНИЕ ДАННЫМИ
"""


# # создать объекты
# user = User("user1")
# quiz = Quiz("QUIZ 1", user)
# question = Question("Сколько будут 2+2*2", "6", "8", "2", "0")


# # добавить в квиз вопрос
# quiz.question.append(question)

# # сохранить КВИЗ в базу
# db.session.add(quiz)
# db.session.commit()

# # взять все  квизы из базы и распечатать с вопросами
# quizes = Quiz.query.all() #
# for quiz in quizes:
#     print(quiz) # как в __repr__
#     print(quiz.question) # -> список
#     for question in quiz.question:
#         print(question) # как в __repr__


# # взять вопрос по id (так работает только по id) самый быстрый метод
# question = db.session.query(Question).get(id)

# # сколько вопросов в квизе
# len(quiz.question)

# # Добавить в квиз вопрос с id = 1
# quiz.question.append(db.session.query(Question).get(1))
# db.session.commit()

# # найти вопросы id которых есть в списке или не в списке
# questions = Question.query.filter(Question.id.in_([1,2,3])).all()
# questions = Question.query.filter(Question.id.not_in([1,2,3])).all()

# # изменить данные
# question = db.session.query(Question).get(id)
# question.question = 'измененный вопрос'
# question.answer = 'измененный правильный ответ'
# user.name = "Vasya"
# db.session.commit()

# # удалить квиз
# Quiz.query.filter_by(id = id).delete()
# db.session.query(Quiz).get(id).delete()
# db.session.commit()

# # отвязать вопрос от квиза
# question = db.session.query(Question).get(id)
# quiz.question.remove(question)
# db.session.commit()


# """
