from datetime import datetime, timezone

from dateutil import parser
from pydantic import BaseModel, constr, root_validator

from backend.schemas.category import CategoryInDBBase
from backend.schemas.place import PlaceInDBBase
from backend.schemas.organization import OrganizationInDBBase
from backend.schemas.user import UserInDBBase


class EventBase(BaseModel):
    title: constr(max_length=100)
    description: constr(max_length=1000)
    date_begin: datetime
    date_end: datetime
    place_description: constr(max_length=100)
    tags: list[constr(max_length=15)]


class EventCreate(EventBase):
    place_id: int
    category_id: int
    organization_id: int | None

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
    user: UserInDBBase
    organization: OrganizationInDBBase | None
    place: PlaceInDBBase
    category: CategoryInDBBase
    participant_count: int

    class Config:
        orm_mode = True
