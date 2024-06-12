from pydantic import BaseModel, Field

from app.schemas.common import PyObjectId


class DealBase(BaseModel):
    title: str
    description: str
    customer_id: PyObjectId
    performer_id: PyObjectId


class DealCreate(DealBase):
    pass


class Deal(DealBase):
    id: PyObjectId = Field(alias="_id")
    completed: bool

    class Config:
        orm_mode = True
