from bson import ObjectId
from fastapi import APIRouter, HTTPException, status, Request

from app.schemas.deals import DealCreate, Deal

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.get("/", summary="Get list of deals", response_model=list[Deal])
async def get_deals(request: Request):
    deals = await request.app.mongodb["orders"].find().to_list(1000)
    return deals


@router.get("/{id}", summary="Get deal by id", response_model=Deal)
async def get_order(id: str, request: Request):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ObjectId")

    deal = await request.app.mongodb["deals"].find_one({"_id": ObjectId(id)})
    if not deal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Deal not found")
    return deal


@router.patch("/{id}", response_model=Deal, summary="Mark deal as completed")
async def mark_order_as_completed(id: str, request: Request):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ObjectId")

    deal = await request.app.mongodb["deals"].find_one({"_id": ObjectId(id)})
    if not deal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Deal not found")

    update_data = {
        "completed": True
    }
    await request.app.mongodb["deals"].update_one(
        {"_id": ObjectId(id)},
        {"$set": update_data},
    )

    updated_deal = await request.app.mongodb["deals"].find_one({"_id": ObjectId(id)})
    return updated_deal


@router.post("/", response_model=Deal, summary="Create a new deal")
async def create_deal(deal: DealCreate, request: Request):
    try:
        customer_id = ObjectId(deal.customer_id)
        performer_id = ObjectId(deal.performer_id)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ObjectId")

    customer = await request.app.mongodb["users"].find_one({"_id": customer_id})
    if customer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")

    performer = await request.app.mongodb["users"].find_one({"_id": performer_id})
    if performer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Performer not found")

    new_deal = await request.app.mongodb["deals"].insert_one({
        **deal.model_dump(),
        "customer_id": customer_id,
        "performer_id": performer_id,
        "completed": False,
    })
    created_deal = await request.app.mongodb["deals"].find_one(
        {"_id": new_deal.inserted_id}
    )

    return created_deal
