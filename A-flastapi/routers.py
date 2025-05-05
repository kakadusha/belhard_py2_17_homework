from fastapi import APIRouter, Depends, HTTPException
from schema import *
from database import UserRepository, GalleryRepository, PaintingRepository

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
    users = await UserRepository.get_users()
    return list(map(DataClassUserGet.model_validate, users))


@users_router.get("/{id}")
async def get_user(id) -> DataClassUserGet:
    user = await UserRepository.get_user(id=id)
    if user:
        return DataClassUserGet.model_validate(user)
    # return {'err':"User not found"} # но тогда get_user(id) -> User | dict[str,str]
    raise HTTPException(status_code=404, detail="User not found")


@users_router.post("")
async def post_user(user: DataClassUserAdd = Depends()) -> DataClassUserId:
    id = await UserRepository.add_user(user)
    # return {"id": id}
    return DataClassUserId(id=id)


######### gallery_router ##########

gallery_router = APIRouter(
    prefix="/gallery", tags=["Галерея"]  # слэш оставляем открытыми
)


@gallery_router.get("")
async def get_galleries() -> list[DataClassGalleryList]:
    galleries = await GalleryRepository.get_galleries()
    return list(map(DataClassGalleryList.model_validate, galleries))


# не работает c paintings, падает потому что не может загрузить
# is not bound to a Session; lazy load operation of attribute 'paintings'
# cannot proceed (Background on this error at: https://sqlalche.me/e/20/bhk3)"
@gallery_router.get("/{gallery_id}")
async def get_gallery(gallery_id: int):
    gallery = await GalleryRepository.get_gallery(gallery_id)
    return gallery


# реализован вложенный запрос
@gallery_router.get("/{gallery_id}/paintings")
async def get_gallery_with_paintings(gallery_id: int):
    gallery = await GalleryRepository.get_gallery_with_paintings(gallery_id)
    return gallery


@gallery_router.post("")
async def post_gallery(gallery: DataClassGalleryAdd = Depends()) -> DataClassGalleryGet:
    id = await GalleryRepository.add_gallery(gallery)
    return DataClassGalleryGet(id=id, **gallery.model_dump())


######### painting_router ##########

painting_router = APIRouter(
    prefix="/painting", tags=["Картина"]  # слэш оставляем открытыми
)


@painting_router.get("")
async def get_paintings() -> list[DataClassPaintingGet]:
    paintings = await PaintingRepository.get_paintings()
    return list(map(DataClassPaintingGet.model_validate, paintings))


@painting_router.get("/{id}")
async def get_painting(id) -> DataClassPaintingGet:
    painting = await PaintingRepository.get_painting(id=id)
    if painting:
        return DataClassPaintingGet.model_validate(painting)
    raise HTTPException(status_code=404, detail="Painting not found")


@painting_router.post("")
async def post_painting(
    painting: DataClassPaintingAdd = Depends(),
) -> DataClassPaintingGet:
    id = await PaintingRepository.add_painting(painting)
    # return {"id": id}
    return DataClassPaintingGet(id=id, **painting.model_dump())
