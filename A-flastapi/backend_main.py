# pip install fastapi,  uvicorn, pydantic, aiosqlite, sqlalchemy'''
"""
FastAPI
ендпоинты:

** Пользователь **
GET     /api/users              Get all
GET     /api/users/{id}         Get by ID
POST    /api/users              Create new

** Картина **
GET     /api/painting           Get all paintings
POST    /api/painting           Add new painting
GET     /api/painting/{id}      Get painting by ID
DELETE  /api/painting/{id}      Delete painting by ID

** Галерея **
GET     /api/gallery                                        Get all
GET     /api/gallery/{gallery_id}                           Get by ID
POST    /api/gallery                                        Create new
DELETE  /api/gallery/{gallery_id}                           Delete by ID
GET     /api/gallery/{gallery_id}/paintings                 Get Gallery With Paintings
PUT     /api/gallery/{gallery_id}/painting/{painting_id}    Put painting to gallery
"""

from fastapi import FastAPI
from routers import users_router, default_router, gallery_router, painting_router
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
app.include_router(gallery_router)
app.include_router(painting_router)


if __name__ == "__main__":
    uvicorn.run("backend_main:app", reload=True, port=8200)
    # uvicorn.run ("other_folder.main:app", reload=True, port=8500)


# uvicorn backend_main:app --host 0.0.0.0 --port 8000 --reload
