from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db import models
from app.db.connection import get_db
from app.schemas.orders import OrderCreate, Order

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.get("/", summary="Get list of orders", response_model=list[Order])
def get_orders(db: Session = Depends(get_db)):
    orders = db.query(models.Orders).all()
    return orders


@router.get("/{id}", summary="Get order by id", response_model=Order)
def get_order(id: int, db: Session = Depends(get_db)):
    order = db.query(models.Orders).filter(models.Orders.id == id).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return order


@router.patch("/{id}", response_model=Order, summary="Mark order as completed")
def mark_order_as_completed(id: int, db: Session = Depends(get_db)):
    db_order = db.query(models.Orders).filter(models.Orders.id == id).first()
    if not db_order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

    db_order.completed = True

    db.commit()
    db.refresh(db_order)
    return db_order


@router.post("/", response_model=Order, summary="Create a new order")
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    customer = db.query(models.Users).filter(models.Users.id == order.customer_id).first()
    if customer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")

    performer = db.query(models.Users).filter(models.Users.id == order.performer_id).first()
    if performer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Performer not found")

    new_order = models.Orders(**order.model_dump())
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order
