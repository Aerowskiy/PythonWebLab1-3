from typing import Optional

from pydantic import BaseModel


class DealBase(BaseModel):
    title: str
    description: str
    customer_id: int
    performer_id: int


class DealCreate(DealBase):
    pass


class Deal(DealBase):
    id: int
    completed: bool

    class Config:
        orm_mode = True
