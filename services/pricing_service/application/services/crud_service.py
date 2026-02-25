from services.pricing_service.infrastructure.db.schema import PricingModel
from services.pricing_service.infrastructure.db.repository import PricingRepository
from services.pricing_service.application.dtos import (
    CreatePricingDTO,
    UpdatePricingDTO,
    PricingResponseDTO,
)


class PricingService:
    def __init__(self, session):
        self.repo = PricingRepository(session)

    def create(self, dto: CreatePricingDTO) -> PricingResponseDTO:
        pricing = PricingModel(
            product_pk=dto.product_pk,
            price=dto.price,
        )
        created = self.repo.create(pricing)
        return PricingResponseDTO.model_validate(created)

    def get_by_product(self, product_pk: str) -> PricingResponseDTO | None:
        pricing = self.repo.get_by_product(product_pk)
        if pricing is None:
            return None
        return PricingResponseDTO.model_validate(pricing)

    def update_by_product(self, product_pk: str, dto: UpdatePricingDTO) -> PricingResponseDTO | None:
        fields = dto.model_dump(exclude_none=True)
        updated = self.repo.update_by_product(product_pk, **fields)
        if updated is None:
            return None
        return PricingResponseDTO.model_validate(updated)

    def delete(self, product_pk: str) -> bool:
        return self.repo.delete_by_product(product_pk)
