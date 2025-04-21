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
new_session = async_sessionmaker(engine, expire_on_commit=False)


class Model(DeclarativeBase):
    pass


##### USER #####


class UserOrm(Model):
    """Работа на уровне таблиц для User"""

    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    age: Mapped[int]
    phone: Mapped[str | None]
    galleries = relationship(
        "GalleryOrm", backref="user", cascade="all, delete, delete-orphan"
    )


# many_to_many
gallery_painting = Table(
    "gallery_painting",
    Model.metadata,
    Column("gallery_id", Integer, ForeignKey("gallery.id"), primary_key=True),
    Column("painting_id", Integer, ForeignKey("painting.id"), primary_key=True),
)


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
    # Установите связь с GalleryOrm
    # galleries: Mapped[list[GalleryOrm]] = relationship(
    galleries = relationship(
        "GalleryOrm", secondary=gallery_painting, back_populates="paintings"
    )


##### GALLERY #####


class GalleryOrm(Model):
    __tablename__ = "gallery"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    desc: Mapped[str | None] = mapped_column(default=None)
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        default=func.now(), onupdate=func.now()
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    # RE: painting = []
    # Определите связь с PaintingOrm
    paintings: Mapped[list[PaintingOrm]] = relationship(
        "PaintingOrm", secondary=gallery_painting, back_populates="galleries"
    )


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

    @classmethod
    async def get_paintings(cls) -> list[PaintingOrm]:
        async with new_session() as session:
            query = select(PaintingOrm)
            res = await session.execute(query)
            paintings = res.scalars().all()
            # return list
            return list(paintings)


class GalleryRepository:
    """Все про галерею C R U D"""

    @classmethod
    async def add_gallery(cls, gallery: DataClassGalleryAdd) -> int:
        async with new_session() as session:
            data = gallery.model_dump()
            print(data)
            gallery_orm = GalleryOrm(**data)
            session.add(gallery_orm)
            await session.flush()
            await session.commit()
            return gallery_orm.id

    @classmethod
    async def get_gallery(cls, id) -> GalleryOrm | None:
        async with new_session() as session:
            query = select(GalleryOrm).filter(GalleryOrm.id == id)
            res = await session.execute(query)
            gallery = res.scalars().first()
            return gallery

    @classmethod
    async def get_galleries(cls) -> list[GalleryOrm]:
        async with new_session() as session:
            query = select(GalleryOrm)
            res = await session.execute(query)
            galleries = res.scalars().all()
            # return list
            return list(galleries)


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
                size="100x100",
                material="oil",
                technique="canvas",
                desc="testdesc1",
                price="1000",
                status="available",
            ),
            PaintingOrm(
                name="testpainting2",
                image="testimage2",
                size="200x200",
                material="watercolor",
                technique="paper",
                desc="testdesc2",
                price="2000",
                status="sold",
            ),
        ]
        session.add_all(paintings)
        # Сохраняем изменения для получения ID пользователей и картин
        await session.commit()

        # Создаем галереи и устанавливаем связи с картинами
        galleries = [
            GalleryOrm(
                name="testgallery1", user_id=1, paintings=[paintings[0], paintings[1]]
            ),
            GalleryOrm(name="testgallery2", user_id=2, paintings=[paintings[1]]),
        ]
        session.add_all(galleries)
        # Сохраняем изменения
        await session.flush()
        await session.commit()
