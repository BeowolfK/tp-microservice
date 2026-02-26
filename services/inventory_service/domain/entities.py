from uuid import UUID, uuid4
from pydantic import BaseModel, Field


class Warehouse(BaseModel):
    """Warehouse entity model.

    Represents a warehouse location where inventory is stored.
    """
    id: UUID = Field(default_factory=uuid4)
    name: str = Field(min_length=1, max_length=100)
    location: str = Field(default="", max_length=200)


class InventoryItem(BaseModel):
    """Inventory item entity model.

    Represents the quantity of a product stored in a specific warehouse.
    """
    id: UUID = Field(default_factory=uuid4)
    product_pk: str
    warehouse_pk: str
    quantity: int = Field(default=0)
