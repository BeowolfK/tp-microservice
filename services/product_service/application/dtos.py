"""DTOs pour le service Product."""

from pydantic import BaseModel, Field, field_validator
from services.product_service.domain.entities import Category


class CreateProductDTO(BaseModel):
    """DTO pour la creation d'un produit."""

    name: str = Field(min_length=1, max_length=100)
    description: str = Field(default="", max_length=1000)
    category: Category
    available: bool = True

    @field_validator("name")
    @classmethod
    def name_must_not_be_blank(cls, v: str) -> str:
        """Valide que le nom n'est pas vide ou compose uniquement d'espaces."""
        if not v.strip():
            raise ValueError("le nom ne peut pas etre vide")
        return v.strip()


class UpdateProductDTO(BaseModel):
    """DTO pour la mise a jour d'un produit."""

    name: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=1000)
    category: Category | None = None
    available: bool | None = None

    @field_validator("name")
    @classmethod
    def name_must_not_be_blank(cls, v: str | None) -> str | None:
        """Valide que le nom n'est pas vide ou compose uniquement d'espaces."""
        if v is not None and not v.strip():
            raise ValueError("le nom ne peut pas etre vide")
        return v.strip() if v else v


class ProductResponseDTO(BaseModel):
    """DTO de reponse pour un produit."""

    id: str
    name: str
    description: str
    category: Category
    available: bool

    model_config = {"from_attributes": True}
