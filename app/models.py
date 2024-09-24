import enum
from datetime import datetime

from sqlalchemy import Column, Integer, String, Float, DateTime, Enum, ForeignKey, func
from sqlalchemy.orm import relationship

from app.database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True)
    price = Column(Float, nullable=False)
    description = Column(String)
    stock_quantity = Column(Integer, nullable=False, index=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    product_items = relationship("OrderItem", back_populates="product")


class OrderStatusEnum(str, enum.Enum):
    processing = "в процессе"
    shipped = "отправлен"
    delivered = "доставлен"


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    status = Column(Enum(OrderStatusEnum), default=OrderStatusEnum.processing)
    order_items = relationship("OrderItem", back_populates="order")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    order_items = relationship("OrderItem", back_populates="order")


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), index=True)
    product_id = Column(Integer, ForeignKey("products.id"), index=True)
    quantity = Column(Integer)

    order = relationship("Order", back_populates="order_items")
    product = relationship("Product", back_populates="product_items")
