from pydantic import BaseModel, Field, field_validator


class CreateCustomerDTO(BaseModel):
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    email: str = Field(min_length=1, max_length=255)

    @field_validator("first_name")
    @classmethod
    def first_name_must_not_be_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("le prénom ne peut pas etre vide")
        return v.strip()

    @field_validator("last_name")
    @classmethod
    def last_name_must_not_be_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("le nom ne peut pas etre vide")
        return v.strip()


class UpdateCustomerDTO(BaseModel):
    first_name: str | None = Field(default=None, min_length=1, max_length=100)
    last_name: str | None = Field(default=None, min_length=1, max_length=100)
    email: str | None = Field(default=None, min_length=1, max_length=255)

    @field_validator("first_name")
    @classmethod
    def first_name_must_not_be_blank(cls, v: str | None) -> str | None:
        if v is not None and not v.strip():
            raise ValueError("le prénom ne peut pas etre vide")
        return v.strip() if v else v

    @field_validator("last_name")
    @classmethod
    def last_name_must_not_be_blank(cls, v: str | None) -> str | None:
        if v is not None and not v.strip():
            raise ValueError("le nom ne peut pas etre vide")
        return v.strip() if v else v


class CustomerResponseDTO(BaseModel):
    id: str
    first_name: str
    last_name: str
    email: str

    model_config = {"from_attributes": True}
