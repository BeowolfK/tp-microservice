from uuid import UUID, uuid4
from enum import StrEnum
from pydantic import BaseModel, Field, field_validator


class Category(StrEnum):
    ELECTRONICS = "electronics"
    CLOTHING = "clothing"
    FOOD = "food"
    BOOKS = "books"
    OTHER = "other"


class Product(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str = Field(min_length=1, max_length=100)
    description: str = Field(default="", max_length=1000)
    category: Category
    available: bool = True

    @field_validator("name")
    @classmethod
    def name_must_not_be_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("le nom ne peut pas etre vide")
        return v.strip()
