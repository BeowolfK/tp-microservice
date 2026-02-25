from pydantic import BaseModel, Field
from services.order_service.domain.entities import OrderStatus


class CreateOrderLineDTO(BaseModel):
    product_pk: str
    quantity: int
    unit_price: float


class CreateOrderDTO(BaseModel):
    customer_pk: str
    lines: list[CreateOrderLineDTO]


class UpdateOrderDTO(BaseModel):
    status: OrderStatus | None = None


class OrderLineResponseDTO(BaseModel):
    id: str
    order_pk: str
    product_pk: str
    quantity: int
    unit_price: float

    model_config = {"from_attributes": True}


class OrderResponseDTO(BaseModel):
    id: str
    customer_pk: str
    status: str
    created_at: str
    lines: list[OrderLineResponseDTO]

    model_config = {"from_attributes": True}
