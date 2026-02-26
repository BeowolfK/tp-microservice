from uuid import UUID, uuid4
from enum import StrEnum
from datetime import datetime
from pydantic import BaseModel, Field


class OrderStatus(StrEnum):
    """Order status enumeration.

    Defines the possible states of an order throughout its lifecycle.
    """
    PENDING = "pending"
    CONFIRMED = "confirmed"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class OrderLine(BaseModel):
    """Order line item entity model.

    Represents a single product line item within an order.
    """
    id: UUID = Field(default_factory=uuid4)
    order_pk: str
    product_pk: str
    quantity: int
    unit_price: float


class Order(BaseModel):
    """Order entity model.

    Represents a customer order with status tracking and timestamps.
    """
    id: UUID = Field(default_factory=uuid4)
    customer_pk: str
    status: OrderStatus = OrderStatus.PENDING
    created_at: datetime = Field(default_factory=datetime.now)
