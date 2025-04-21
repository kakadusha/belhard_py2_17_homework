from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import select, Integer, ForeignKey, String, Table, Column, func
from datetime import datetime

from schema import *

import os

BASE_DIR = os.path.dirname(__file__)
DB_DIR = os.path.join(BASE_DIR, "db")

if not os.path.exists(DB_DIR):
    os.makedirs(DB_DIR)

DB_PATH = os.path.join(DB_DIR, "fastapi.db")

engine = create_async_engine(f"sqlite+aiosqlite:///{DB_PATH}")
# engine = create_async_engine("sqlite+aiosqlite:///example//fastapi//db//fastapi.db")
# engine = create_async_engine("sqlite+aiosqlite:///db//fastapi.db")
new_session = async_sessionmaker(engine, expire_on_commit=False)


class Model(DeclarativeBase):
    pass


#    # можно тут добавить тогда эти столбцы будут во всех таблицах
#    # т.к. мы наследуемся от этого класса

#     id: Mapped[int] = mapped_column(primary_key=True)

#     # будет вписывать дататайм при создании записи
#     dateCreate: Mapped[datetime] = mapped_column(
#                                         server_default=func.now(),
#                                         nullable=False)

#     # будет вписывать дататайм при обновлении записи
#     dateUpdate: Mapped[datetime] = mapped_column(
#                                         server_default=func.now(),
#                                         server_onupdate=func.now(),
#                                         nullable=False)


##### USER #####


class UserOrm(Model):
    """Работа на уровне таблиц для User"""

    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    age: Mapped[int]
    phone: Mapped[str | None]
    # quiz = relationship('QuizOrm', backref='user')
    galleries = relationship(
        "GalleryOrm", backref="user", cascade="all, delete, delete-orphan"
    )


# many_to_many
gallery_painting = Table(
    "gallery_painting",
    Column("gallery_id", Integer, ForeignKey("gallery.id"), primary_key=True),
    Column("painting_id", Integer, ForeignKey("painting.id"), primary_key=True),
)
# class GalleryPaintingOrm(Model):
#     __tablename__ = "gallery_painting"
#     # id: Mapped[int] = mapped_column(primary_key=True)
#     gallery_id: Mapped[int] = mapped_column(ForeignKey("gallery.id"), primary_key=True)
#     painting_id: Mapped[int] = mapped_column(
#         ForeignKey("painting.id"), primary_key=True
#     )


##### PAINTING #####
class PaintingOrm(Model):
    """Работа на уровне таблиц для Painting"""

    __tablename__ = "painting"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    image: Mapped[str]
    size: Mapped[str]
    material: Mapped[str]
    technique: Mapped[str]
    desc: Mapped[str]
    price: Mapped[str]
    status: Mapped[str]
    # Эта строка устанавливает двустороннюю связь между Painting и Gallery.
    # Вы можете получить список тестов, связанных с вопросом, через question_instance.quiz,
    # и список вопросов, связанных с тестом, через quiz_instance.question.
    # backref делает код более чистым и удобным в использовании, избегая сложных запросов к базе данных
    # RE
    # gallery = db.relationship("Gallery", secondary=gallery_painting, backref="painting")
    gallery = relationship("GalleryOrm", secondary=gallery_painting, backref="painting")


##### GALLERY #####


class GalleryOrm(Model):
    __tablename__ = "gallery"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    # RE: painting = []

    # we need here list of PaintingOrm
    # paintings: Mapped[list[PaintingOrm]] = relationship(
    #     "PaintingOrm",
    #     secondary="gallery_painting",
    #     backref="galleries",
    #     # cascade="all, delete, delete-orphan",  # орфана раньше не было
    # )
    painting: Mapped[list[PaintingOrm]]


#### REPOS ####


class UserRepository:
    """Все про юзера C R U D"""

    @classmethod
    async def add_user(cls, user: DataClassUserAdd) -> int:
        async with new_session() as session:
            data = user.model_dump()
            print(data)
            user_orm = UserOrm(**data)
            session.add(user_orm)
            await session.flush()
            await session.commit()
            return user_orm.id

    @classmethod
    async def get_users(cls) -> list[UserOrm]:
        async with new_session() as session:
            query = select(UserOrm)
            res = await session.execute(query)
            users = res.scalars().all()
            # return list
            return list(users)

    @classmethod
    async def get_user(cls, id) -> UserOrm | None:
        async with new_session() as session:
            query = select(UserOrm).filter(UserOrm.id == id)
            # query = text(f"SELECT * FROM users WHERE id={id}")
            res = await session.execute(query)
            user = res.scalars().first()
            return user


class PaintingRepository:
    """Все про картину C R U D"""

    @classmethod
    async def add_painting(cls, painting: DataClassPaintingAdd) -> int:
        async with new_session() as session:
            data = painting.model_dump()
            print(data)
            painting_orm = PaintingOrm(**data)
            session.add(painting_orm)
            await session.flush()
            await session.commit()
            return painting_orm.id

    @classmethod
    async def get_painting(cls, id) -> PaintingOrm | None:
        async with new_session() as session:
            query = select(PaintingOrm).filter(PaintingOrm.id == id)
            res = await session.execute(query)
            painting = res.scalars().first()
            return painting


#### functions #####


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)


async def delete_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)


async def add_test_data():
    async with new_session() as session:
        users = [
            UserOrm(name="testuser1", age=20),
            UserOrm(name="testuser2", age=30, phone="123456789"),
        ]
        session.add_all(users)

        paintings = [
            PaintingOrm(
                name="testpainting1",
                image="testimage1",
                size="testsize1",
                material="testmaterial1",
                technique="testtechnique1",
                desc="testdesc1",
                price="testprice1",
                status="teststatus1",
            ),
            PaintingOrm(
                name="testpainting2",
                image="testimage2",
                size="testsize2",
                material="testmaterial2",
                technique="testtechnique2",
                desc="testdesc2",
                price="testprice2",
                status="teststatus2",
            ),
        ]
        session.add_all(paintings)

        galleries = [
            GalleryOrm(name="testgallery1", user_id=1),
            GalleryOrm(name="testgallery2", user_id=2),
        ]
        session.add_all(galleries)

        # gallery_painting = [
        #     GalleryPaintingOrm(gallery_id=1, painting_id=1),
        #     GalleryPaintingOrm(gallery_id=1, painting_id=2),
        #     GalleryPaintingOrm(gallery_id=2, painting_id=1),
        # ]
        # session.add_all(gallery_painting)

        await session.flush()
        await session.commit()
