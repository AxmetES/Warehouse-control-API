from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import schemas, models
from app.database import get_db
from app.settings import logger

orders_router = APIRouter()


@orders_router.post("/orders", response_model=schemas.OrderResponse)
def create_order(order: schemas.OrderCreate, db:Session = Depends(get_db)):
    try:
        new_order = models.Order()
        db.add(new_order)
        db.commit()
        db.refresh(new_order)
        for item in order.order_items:
            product = db.query(models.Product).filter(
                models.Product.id == item.product_id).first()
            if not product:
                logger.warn(f"Product with ID {item.product_id} not found")
                raise HTTPException(
                    status_code=404,
                    detail=f"Product with ID {item.product_id} not found")

            if product.stock_quantity < item.quantity:
                logger.warn(f'''Not enough stock for product ID {item.product_id}
                in order:{item.quantity}, in stock:{product.stock_quantity}''')
                raise HTTPException(
                    status_code=400,
                    detail=f'''Not enough stock for product ID {item.product_id}, in order:{item.quantity}, in stock:{product.stock_quantity}''')

            product.stock_quantity -= item.quantity
            order_item = models.OrderItem(
                order_id=new_order.id,
                product_id=product.id,
                quantity=item.quantity
            )
            db.add(product)
            db.add(order_item)
        db.commit()
        db.refresh(new_order)
        return new_order
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail="Server error")


@orders_router.get("/orders", response_model=List[schemas.OrderResponse])
def get_orders(db: Session = Depends(get_db)):
    orders = db.query(models.Order).all()
    return orders


@orders_router.get("/orders/{order_id}", response_model=schemas.OrderResponse)
def get_order(order_id: int, db: Session = Depends(get_db)):
    try:
        order = db.query(models.Order).filter(models.Order.id == order_id).first()
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        return order
    except Exception as e:
        raise HTTPException(status_code=500, detail="Order not found")


@orders_router.patch("/orders/{id}/status", response_model=schemas.OrderResponse)
def update_order_status(id: int, status_update: schemas.OrderStatusUpdate, db: Session = Depends(get_db)):
    try:
        order = db.query(models.Order).filter(models.Order.id == id).first()
        if not order:
            raise HTTPException(status_code=404, detail=f"Order not found")
        order.status = status_update.status
        db.commit()
        db.refresh(order)
        return order
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error")
