from pydantic import BaseModel, field_validator, Field
from app.schemas.common import PyObjectId


class ReviewBase(BaseModel):
    text: str
    rating: int
    user_id: PyObjectId
    reviewer_id: PyObjectId

    @field_validator('rating')
    def validate_rating(cls, value):
        if value not in range(1, 6):
            raise ValueError('Rating must be from 1 to 5')
        return value


class ReviewCreate(ReviewBase):
    pass


class Review(ReviewBase):
    id: PyObjectId = Field(alias="_id")

    class Config:
        orm_mode = True
