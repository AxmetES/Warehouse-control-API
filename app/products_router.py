from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import schemas, models
from app.database import get_db
from app.settings import logger

products_router = APIRouter()


@products_router.post("/products", response_model=schemas.ProductResponse)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    try:
        existing_product = db.query(models.Product).filter(
            models.Product.name == product.name).first()
        if existing_product:
            logger.warn(f"Product name exists. name -- {product.name}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Product with this name already exists"
            )
        new_product = models.Product(**product.dict())
        db.add(new_product)
        db.commit()
        db.refresh(new_product)
        return new_product

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"Unexpected error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected server error occurred")


@products_router.get("/products", response_model=List[schemas.ProductResponse])
def get_products(db: Session = Depends(get_db)):
    try:
        products = db.query(models.Product).all()
        return products
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail="Server error")


@products_router.get("/products/{id}", response_model=schemas.ProductResponse)
def get_product(id: int, db: Session = Depends(get_db)):
    try:
        product = db.query(models.Product).filter(
            models.Product.id == id).first()
        if product is None:
            logger.warn(f"Product not found. id: {id}")
            raise HTTPException(status_code=404, detail="Product not found")
        return product
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail="Server error")


@products_router.put("/products/{id}", response_model=schemas.ProductResponse)
def update_product(id: int, product: schemas.ProductUpdate, db: Session = Depends(get_db)):
    try:
        ex_product = db.query(models.Product).filter(models.Product.id == id).first()
        if ex_product is None:
            raise HTTPException(status_code=404, detail="Product not found")
        if product.name is not None:
            ex_product.name = product.name
        if product.description is not None:
            ex_product.description = product.description
        if product.price is not None:
            ex_product.price = float(product.price)
        if product.stock_quantity is not None:
            ex_product.stock_quantity = int(product.stock_quantity)
        db.commit()
        db.refresh(ex_product)
        return ex_product
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail="Server error")


@products_router.delete("/products/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(id: int, db: Session = Depends(get_db)):
    try:
        product = db.query(models.Product).filter(models.Product.id == id).first()
        if product is None:
            logger.warn(f"Attempt to delete non-existent product with id: {id}")
            raise HTTPException(status_code=404, detail="Product not found")

        db.delete(product)
        db.commit()
        logger.info(f"Product id: {id} was successfully deleted.")
        return None

    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail="Server error")
