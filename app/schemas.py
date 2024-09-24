from enum import Enum

from pydantic import BaseModel, conint, ConfigDict
from typing import List, Optional
from datetime import datetime


class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    stock_quantity: conint(ge=0)


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stock_quantity: conint(ge=0)


class ProductResponse(ProductBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class OrderItemBase(BaseModel):
    product_id: int
    quantity: int


class OrderItemCreate(OrderItemBase):
    pass


class OrderItemResponse(OrderItemBase):
    id: int
    product: ProductResponse

    model_config = ConfigDict(from_attributes=True)


class OrderStatusEnum(str, Enum):
    processing = "в процессе"
    shipped = "отправлен"
    delivered = "доставлен"


class OrderBase(BaseModel):
    status: OrderStatusEnum


class OrderCreate(OrderBase):
    order_items: List[OrderItemCreate]


class OrderResponse(OrderBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
    order_items: List[OrderItemResponse]

    model_config = ConfigDict(from_attributes=True)


class OrderStatusUpdate(OrderBase):
    status: OrderStatusEnum

    model_config = ConfigDict(from_attributes=True)
