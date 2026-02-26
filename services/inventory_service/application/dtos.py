from pydantic import BaseModel, Field


class CreateWarehouseDTO(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    location: str = Field(default="", max_length=200)


class WarehouseResponseDTO(BaseModel):
    id: str
    name: str
    location: str

    model_config = {"from_attributes": True}


class CreateInventoryDTO(BaseModel):
    product_pk: str
    warehouse_pk: str
    quantity: int = Field(default=0)


class UpdateInventoryDTO(BaseModel):
    quantity: int


class InventoryResponseDTO(BaseModel):
    id: str
    product_pk: str
    warehouse_pk: str
    quantity: int

    model_config = {"from_attributes": True}
