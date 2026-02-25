from uuid import UUID, uuid4
from enum import StrEnum
from datetime import datetime
from pydantic import BaseModel, Field


class OrderStatus(StrEnum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class OrderLine(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    order_pk: str
    product_pk: str
    quantity: int
    unit_price: float


class Order(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    customer_pk: str
    status: OrderStatus = OrderStatus.PENDING
    created_at: datetime = Field(default_factory=datetime.now)
