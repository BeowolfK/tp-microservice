from services.customer_service.infrastructure.db.schema import CustomerModel
from services.customer_service.infrastructure.db.repository import CustomerRepository
from services.customer_service.application.dtos import (
    CreateCustomerDTO,
    UpdateCustomerDTO,
    CustomerResponseDTO,
)


class CustomerService:
    def __init__(self, session):
        self.repo = CustomerRepository(session)

    def create(self, dto: CreateCustomerDTO) -> CustomerResponseDTO:
        customer = CustomerModel(
            first_name=dto.first_name,
            last_name=dto.last_name,
            email=dto.email,
        )
        created = self.repo.create(customer)
        return CustomerResponseDTO.model_validate(created)

    def get(self, customer_id: str) -> CustomerResponseDTO | None:
        customer = self.repo.get(customer_id)
        if customer is None:
            return None
        return CustomerResponseDTO.model_validate(customer)

    def get_all(self) -> list[CustomerResponseDTO]:
        customers = self.repo.get_all()
        return [CustomerResponseDTO.model_validate(c) for c in customers]

    def update(self, customer_id: str, dto: UpdateCustomerDTO) -> CustomerResponseDTO | None:
        fields = dto.model_dump(exclude_none=True)
        updated = self.repo.update(customer_id, **fields)
        if updated is None:
            return None
        return CustomerResponseDTO.model_validate(updated)

    def delete(self, customer_id: str) -> bool:
        return self.repo.delete(customer_id)
