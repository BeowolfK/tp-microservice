from services.pricing_service.infrastructure.db.schema import PricingModel
from services.pricing_service.infrastructure.db.repository import PricingRepository
from services.pricing_service.application.dtos import (
    CreatePricingDTO,
    UpdatePricingDTO,
    PricingResponseDTO,
)


class PricingService:
    """Service layer for managing pricing operations.

    Handles business logic for pricing CRUD operations using the
    pricing repository.
    """
    def __init__(self, session):
        """Initialize PricingService with a database session.

        Parameters:
            session: SQLAlchemy database session.

        Returns:
            None
        """
        self.repo = PricingRepository(session)

    def create(self, dto: CreatePricingDTO) -> PricingResponseDTO:
        """Create a new pricing entry.

        Parameters:
            dto (CreatePricingDTO): Data transfer object containing
                pricing creation data.

        Returns:
            PricingResponseDTO: The created pricing response.
        """
        pricing = PricingModel(
            product_pk=dto.product_pk,
            price=dto.price,
        )
        created = self.repo.create(pricing)
        return PricingResponseDTO.model_validate(created)

    def get_by_product(self, product_pk: str) -> PricingResponseDTO | None:
        """Retrieve pricing information for a product.

        Parameters:
            product_pk (str): The product primary key.

        Returns:
            PricingResponseDTO | None: The pricing response if found,
                None otherwise.
        """
        pricing = self.repo.get_by_product(product_pk)
        if pricing is None:
            return None
        return PricingResponseDTO.model_validate(pricing)

    def update_by_product(self, product_pk: str, dto: UpdatePricingDTO) -> PricingResponseDTO | None:
        """Update pricing for a product.

        Parameters:
            product_pk (str): The product primary key.
            dto (UpdatePricingDTO): Data transfer object containing
                updated pricing data.

        Returns:
            PricingResponseDTO | None: The updated pricing response if
                found, None otherwise.
        """
        fields = dto.model_dump(exclude_none=True)
        updated = self.repo.update_by_product(product_pk, **fields)
        if updated is None:
            return None
        return PricingResponseDTO.model_validate(updated)

    def delete(self, product_pk: str) -> bool:
        """Delete pricing information for a product.

        Parameters:
            product_pk (str): The product primary key.

        Returns:
            bool: True if deletion was successful, False if pricing
                not found.
        """
        return self.repo.delete_by_product(product_pk)
