from pydantic import BaseModel, constr


class PlaceBase(BaseModel):
    label: constr(max_length=100)
    latitude: float
    longitude: float


class PlaceCreate(PlaceBase):
    pass


class PlaceUpdate(PlaceCreate):
    pass


class PlaceInDBBase(PlaceBase):
    id: int

    class Config:
        orm_mode = True
