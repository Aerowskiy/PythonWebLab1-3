from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db import models
from app.db.connection import get_db
from app.schemas.deals import DealCreate, Deal

router = APIRouter(prefix="/deals", tags=["Deals"])


@router.get("/", summary="Get list of deals", response_model=list[Deal])
def get_deal(db: Session = Depends(get_db)):
    deals = db.query(models.Deals).all()
    return deals


@router.get("/{id}", summary="Get deal by id", response_model=Deal)
def get_deal(id: int, db: Session = Depends(get_db)):
    deal = db.query(models.Deals).filter(models.Deals.id == id).first()
    if not deal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Deal not found")
    return deal


@router.patch("/{id}", response_model=Deal, summary="Mark deal as completed")
def mark_deal_as_completed(id: int, db: Session = Depends(get_db)):
    db_deal = db.query(models.Deals).filter(models.Deals.id == id).first()
    if not db_deal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Deal not found")

    db_deal.completed = True

    db.commit()
    db.refresh(db_deal)
    return db_deal


@router.post("/", response_model=Deal, summary="Create a new deal")
def create_deal(deal: DealCreate, db: Session = Depends(get_db)):
    customer = db.query(models.Users).filter(models.Users.id == deal.customer_id).first()
    if customer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Deal not found")

    performer = db.query(models.Users).filter(models.Users.id == deal.performer_id).first()
    if performer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Performer not found")

    new_deal = models.Deals(**deal.model_dump())
    db.add(new_deal)
    db.commit()
    db.refresh(new_deal)
    return new_deal
