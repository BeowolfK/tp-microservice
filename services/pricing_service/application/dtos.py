from pydantic import BaseModel


class CreatePricingDTO(BaseModel):
    product_pk: str
    price: float


class UpdatePricingDTO(BaseModel):
    price: float | None = None


class PricingResponseDTO(BaseModel):
    id: str
    product_pk: str
    price: float

    model_config = {"from_attributes": True}
