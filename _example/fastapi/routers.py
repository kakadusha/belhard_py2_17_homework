from fastapi import APIRouter, Depends, HTTPException
from schema import *
from database import UserRepository as ur

######### default_router ##########

default_router = APIRouter()


@default_router.get("/", tags=["api"])
async def index():
    return {"data": "ok"}


######### user_router ##########

users_router = APIRouter(
    prefix="/users", tags=["Пользователи"]  # слэш оставляем открытыми
)


@users_router.get("")
async def get_users() -> list[DataClassUserGet]:
    users = await ur.get_users()
    return list(map(DataClassUserGet.model_validate, users))


@users_router.get("/{id}")
async def get_user(id) -> DataClassUserGet:
    user = await ur.get_user(id=id)
    if user:
        return DataClassUserGet.model_validate(user)
    # return {'err':"User not found"} # но тогда get_user(id) -> User | dict[str,str]
    raise HTTPException(status_code=404, detail="User not found")


@users_router.post("")
async def post_user(user: DataClassUserAdd = Depends()) -> DataClassUserId:
    id = await ur.add_user(user)
    # return {"id": id}
    return DataClassUserId(id=id)
