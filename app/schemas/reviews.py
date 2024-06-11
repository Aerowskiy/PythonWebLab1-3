from pydantic import BaseModel, field_validator


class ReviewBase(BaseModel):
    text: str
    rating: int
    user_id: int
    reviewer_id: int

    @field_validator('rating')
    def validate_rating(cls, value):
        if value not in range(1, 6):
            raise ValueError('Rating must be from 1 to 5')
        return value


class ReviewCreate(ReviewBase):
    pass


class Review(ReviewBase):
    id: int

    class Config:
        orm_mode = True
