from bson import ObjectId
from fastapi import APIRouter, HTTPException, status, Response, Request

from app.schemas.users import User, UserCreate, UserUpdate

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", summary="Get list of users", response_model=list[User])
async def get_users(request: Request):
    users = await request.app.mongodb["users"].find().to_list(1000)
    return users


@router.get("/{id}", summary="Get user by id", response_model=User)
async def get_user(id: str, request: Request):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ObjectId")

    user = await request.app.mongodb["users"].find_one({"_id": ObjectId(id)})
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.post("/", summary="Create a new user", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(request: Request, user: UserCreate):
    existing_user = await request.app.mongodb["users"].find_one({"username": user.username})
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")

    new_user = await request.app.mongodb["users"].insert_one(user.model_dump())
    created_user = await request.app.mongodb["users"].find_one(
        {"_id": new_user.inserted_id}
    )

    return created_user


@router.patch("/{id}", response_model=User, summary="Update user")
async def update_user(id: str, user_update: UserUpdate, request: Request):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ObjectId")

    db_user = await request.app.mongodb["users"].find_one({"_id": ObjectId(id)})
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    update_data = user_update.model_dump(exclude_unset=True)
    await request.app.mongodb["users"].update_one(
        {"_id": ObjectId(id)},
        {"$set": update_data}
    )

    updated_user = await request.app.mongodb["users"].find_one({"_id": ObjectId(id)})
    return updated_user


@router.delete("/{id}", summary="Delete user", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id: str, request: Request):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ObjectId")

    db_user = await request.app.mongodb["users"].find_one({"_id": ObjectId(id)})
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    await request.app.mongodb["users"].delete_one({"_id": ObjectId(id)})
    return Response(status_code=status.HTTP_204_NO_CONTENT)
