from uuid import UUID, uuid4
from pydantic import BaseModel, Field


class Pricing(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    product_pk: str
    price: float
