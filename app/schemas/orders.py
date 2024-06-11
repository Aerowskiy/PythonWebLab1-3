from typing import Optional

from pydantic import BaseModel


class OrderBase(BaseModel):
    title: str
    description: str
    customer_id: int
    performer_id: int


class OrderCreate(OrderBase):
    pass


class Order(OrderBase):
    id: int
    completed: bool

    class Config:
        orm_mode = True