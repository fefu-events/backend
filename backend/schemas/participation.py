from pydantic import BaseModel, constr


class ParticipationBase(BaseModel):
    event_id: int


class ParticipationCreate(ParticipationBase):
    pass


class ParticipationInDBBase(ParticipationBase):
    user_id: int

    class Config:
        orm_mode = True
