from uuid import UUID, uuid4
from enum import StrEnum
from pydantic import BaseModel, Field, field_validator


class Category(StrEnum):
    """Product category enumeration.

    Defines the available product categories.
    """
    ELECTRONICS = "electronics"
    CLOTHING = "clothing"
    FOOD = "food"
    BOOKS = "books"
    OTHER = "other"


class Product(BaseModel):
    """Product entity model.

    Represents a product with inventory and availability information.
    The product name is validated to ensure it is not empty.
    """
    id: UUID = Field(default_factory=uuid4)
    name: str = Field(min_length=1, max_length=100)
    description: str = Field(default="", max_length=1000)
    category: Category
    available: bool = True

    @field_validator("name")
    @classmethod
    def name_must_not_be_blank(cls, v: str) -> str:
        """Validate that product name is not blank or whitespace.

        Parameters:
            v (str): The product name value to validate.

        Returns:
            str: The stripped product name.

        Raises:
            ValueError: If the product name is blank or only whitespace.
        """
        if not v.strip():
            raise ValueError("le nom ne peut pas etre vide")
        return v.strip()
