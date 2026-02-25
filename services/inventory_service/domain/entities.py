from uuid import UUID, uuid4
from pydantic import BaseModel, Field


class Warehouse(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str = Field(min_length=1, max_length=100)
    location: str = Field(default="", max_length=200)


class InventoryItem(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    product_pk: str
    warehouse_pk: str
    quantity: int = Field(default=0)
