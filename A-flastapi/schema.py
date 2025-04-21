from pydantic import BaseModel, ConfigDict


class DataClassUserAdd(BaseModel):
    name: str
    age: int
    phone: str | None = None


class DataClassUserGet(DataClassUserAdd):
    # ? не очень понятно почему он от DataClassUserAdd а не от BaseModel...
    id: int
    model_config = ConfigDict(from_attributes=True)


class DataClassUserId(BaseModel):
    id: int


class DataClassPaintingAdd(BaseModel):
    name: str
    image: str
    size: str
    material: str
    technique: str
    desc: str
    price: str
    status: str
