from pydantic import BaseModel, ConfigDict


### User


class pdUserAdd(BaseModel):
    name: str
    age: int
    phone: str | None = None


class pdUserGet(pdUserAdd):
    id: int
    model_config = ConfigDict(from_attributes=True)


class pdUserId(BaseModel):
    id: int


### Painting


class pdPaintingAdd(BaseModel):
    name: str
    image: str
    size: str
    material: str
    technique: str
    desc: str
    price: str
    status: str | None = None


class pdPaintingGet(pdPaintingAdd):
    id: int
    model_config = ConfigDict(from_attributes=True)


### Gallery


class pdGalleryAdd(BaseModel):
    name: str
    user_id: int
    desc: str | None = None


class pdGalleryList(pdGalleryAdd):
    id: int
    model_config = ConfigDict(from_attributes=True)


class pdGalleryGet(pdGalleryAdd):
    id: int
    paintings: list[int] | None = None
    model_config = ConfigDict(from_attributes=True)
