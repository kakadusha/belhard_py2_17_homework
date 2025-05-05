from pydantic import BaseModel, ConfigDict


### User


class DataClassUserAdd(BaseModel):
    name: str
    age: int
    phone: str | None = None


class DataClassUserGet(DataClassUserAdd):
    id: int
    model_config = ConfigDict(from_attributes=True)


class DataClassUserId(BaseModel):
    id: int


### Painting


class DataClassPaintingAdd(BaseModel):
    name: str
    image: str
    size: str
    material: str
    technique: str
    desc: str
    price: str
    status: str | None = None


class DataClassPaintingGet(DataClassPaintingAdd):
    id: int
    model_config = ConfigDict(from_attributes=True)


### Gallery


class DataClassGalleryAdd(BaseModel):
    name: str
    user_id: int
    desc: str | None = None


class DataClassGalleryList(DataClassGalleryAdd):
    id: int
    model_config = ConfigDict(from_attributes=True)


class DataClassGalleryGet(DataClassGalleryAdd):
    id: int
    paintings: list[int] | None = None
    model_config = ConfigDict(from_attributes=True)
