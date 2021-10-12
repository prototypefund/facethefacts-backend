from pydantic import BaseModel
from pydantic.main import BaseConfig
from datetime import date
from typing import Optional, Dict
from typing_extensions import TypedDict


class Country(BaseModel):
    id: int
    label: str

    class Config:
        orm_mode = True


class Committee(BaseModel):
    id: int
    entity_type: str
    label: str

    class Config:
        orm_mode = True


class Poll(BaseModel):
    id: int
    entity_type: str
    label: str
    committee: Optional[Committee]
    field_intro: str
    field_poll_date: date

    class Config:
        orm_mode = True
