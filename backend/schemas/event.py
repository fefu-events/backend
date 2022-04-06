from typing import List
from datetime import datetime, timezone
from dateutil import parser

from pydantic import BaseModel, constr, root_validator


class EventBase(BaseModel):
    title: constr(max_length=100)
    description: constr(max_length=1000)
    date_begin: datetime
    date_end: datetime
    place_description: constr(max_length=100)
    tags: List[constr(max_length=15)]


class EventCreate(EventBase):

    @root_validator(pre=True)
    def date_end_must_be_larger_than_date_begin(cls, v):
        date_begin_parsed = parser.parse(v.get('date_begin'))
        date_end_parsed = parser.parse(v.get('date_end'))
        now = datetime.now(tz=timezone.utc)
        if date_begin_parsed < now:
            raise ValueError(
                "date_begin must be larger than now")
        if date_begin_parsed > date_end_parsed:
            raise ValueError(
                "date_end must be larger than date_begin")
        return v


class EventUpdate(EventCreate):
    pass


class EventInDBBase(EventBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
