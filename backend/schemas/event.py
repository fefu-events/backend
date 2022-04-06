from typing import List
from datetime import datetime

from pydantic import BaseModel, constr


class EventBase(BaseModel):
    title: constr(max_length=100)
    description: constr(max_length=1000)
    date_begin: datetime
    date_end: datetime
    place_description: constr(max_length=100)
    tags: List[constr(max_length=15)]


class EventCreate(EventBase):
    pass


class EventUpdate(EventBase):
    pass


class EventInDBBase(EventBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
