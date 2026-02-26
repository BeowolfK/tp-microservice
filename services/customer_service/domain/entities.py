from uuid import UUID, uuid4
from pydantic import BaseModel, Field, field_validator


class Customer(BaseModel):
    """Customer entity model.

    Represents a customer with contact information. All string fields
    are validated to ensure they are not empty.
    """
    id: UUID = Field(default_factory=uuid4)
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    email: str = Field(min_length=1, max_length=255)

    @field_validator("first_name")
    @classmethod
    def first_name_must_not_be_blank(cls, v: str) -> str:
        """Validate that first_name is not blank or whitespace.

        Parameters:
            v (str): The first name value to validate.

        Returns:
            str: The stripped first name.

        Raises:
            ValueError: If the first name is blank or only whitespace.
        """
        if not v.strip():
            raise ValueError("le prénom ne peut pas etre vide")
        return v.strip()

    @field_validator("last_name")
    @classmethod
    def last_name_must_not_be_blank(cls, v: str) -> str:
        """Validate that last_name is not blank or whitespace.

        Parameters:
            v (str): The last name value to validate.

        Returns:
            str: The stripped last name.

        Raises:
            ValueError: If the last name is blank or only whitespace.
        """
        if not v.strip():
            raise ValueError("le nom ne peut pas etre vide")
        return v.strip()
