# pip install fastapi,  uvicorn, pydantic, aiosqlite, sqlalchemy'''
"""
Доделать в проекте FastAPI следующие ендпоинты:

    - /quizes - get, post           /galleries      [get] [post]
    - /quizes/id - get              /galleries/id   [get]

    - /questions - get, post        /pictires       [get] [post]
    - /questions/id - get           /pictires/id    [get]

"""

from fastapi import FastAPI
from routers import users_router, default_router
import uvicorn
from contextlib import asynccontextmanager
from database import create_tables, delete_tables, add_test_data

import os

BASE_DIR = os.path.dirname(__file__)


@asynccontextmanager  # реагирует на  методы __aenter__() и __aexit__()
async def lifespan(app: FastAPI):
    await create_tables()
    await add_test_data()
    print("------ Tables built -------------")

    yield

    await delete_tables()
    print("------ Tables dropped -----------")


app = FastAPI(lifespan=lifespan)

app.include_router(default_router)
app.include_router(users_router)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, port=8200)
    # uvicorn.run ("other_folder.main:app", reload=True, port=8500)


# uvicorn main:app --host 0.0.0.0 --port 8000 --reload
