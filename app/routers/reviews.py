from bson import ObjectId
from fastapi import APIRouter, HTTPException, status, Request

from app.schemas.reviews import Review, ReviewCreate

router = APIRouter(prefix="/reviews", tags=["Reviews"])


@router.get("/", summary="Get list of reviews", response_model=list[Review])
async def get_reviews(request: Request):
    review = await request.app.mongodb["reviews"].find().to_list(1000)
    return review


@router.get("/{id}", summary="Get review by id", response_model=Review)
async def get_review(id: str, request: Request):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ObjectId")

    review = await request.app.mongodb["reviews"].find_one({"_id": ObjectId(id)})
    if not review:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")
    return review


@router.post("/", summary="Create a new review", response_model=Review)
async def create_review(review: ReviewCreate, request: Request):
    try:
        user_id = ObjectId(review.user_id)
        reviewer_id = ObjectId(review.reviewer_id)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ObjectId")

    user = await request.app.mongodb["users"].find_one({"_id": user_id})
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    reviewer = await request.app.mongodb["users"].find_one({"_id": reviewer_id})
    if reviewer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reviewer not found")

    new_review = await request.app.mongodb["reviews"].insert_one({
        **review.model_dump(),
        "user_id": user_id,
        "reviewer_id": reviewer_id,
    })
    created_review = await request.app.mongodb["reviews"].find_one(
        {"_id": new_review.inserted_id}
    )

    return created_review
