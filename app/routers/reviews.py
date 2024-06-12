from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db import models
from app.db.connection import get_db
from app.schemas.reviews import Review, ReviewCreate

router = APIRouter(prefix="/reviews", tags=["Reviews"])


@router.get("/", summary="Get list of reviews", response_model=list[Review])
def get_reviews(db: Session = Depends(get_db)):
    orders = db.query(models.Reviews).all()
    return orders


@router.get("/{id}", summary="Get review by id", response_model=Review)
def get_review(id: int, db: Session = Depends(get_db)):
    order = db.query(models.Reviews).filter(models.Reviews.id == id).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")
    return order

@router.post("/", response_model=Review, summary="Create a new review")
def create_review(review: ReviewCreate, db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.id == review.user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    reviewer = db.query(models.Users).filter(models.Users.id == review.reviewer_id).first()
    if reviewer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reviewer not found")

    new_review = models.Reviews(**review.model_dump())
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return new_review
