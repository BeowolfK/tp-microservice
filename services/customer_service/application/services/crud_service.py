from services.customer_service.infrastructure.db.schema import CustomerModel
from services.customer_service.infrastructure.db.repository import CustomerRepository
from services.customer_service.application.dtos import (
    CreateCustomerDTO,
    UpdateCustomerDTO,
    CustomerResponseDTO,
)


class CustomerService:
    """Service layer for managing customer operations.

    Handles business logic for customer CRUD operations using the
    customer repository.
    """
    def __init__(self, session):
        """Initialize CustomerService with a database session.

        Parameters:
            session: SQLAlchemy database session.

        Returns:
            None
        """
        self.repo = CustomerRepository(session)

    def create(self, dto: CreateCustomerDTO) -> CustomerResponseDTO:
        """Create a new customer.

        Parameters:
            dto (CreateCustomerDTO): Data transfer object containing
                customer creation data.

        Returns:
            CustomerResponseDTO: The created customer response.
        """
        customer = CustomerModel(
            first_name=dto.first_name,
            last_name=dto.last_name,
            email=dto.email,
        )
        created = self.repo.create(customer)
        return CustomerResponseDTO.model_validate(created)

    def get(self, customer_id: str) -> CustomerResponseDTO | None:
        """Retrieve a customer by ID.

        Parameters:
            customer_id (str): The unique identifier of the customer.

        Returns:
            CustomerResponseDTO | None: The customer response if found,
                None otherwise.
        """
        customer = self.repo.get(customer_id)
        if customer is None:
            return None
        return CustomerResponseDTO.model_validate(customer)

    def get_all(self) -> list[CustomerResponseDTO]:
        """Retrieve all customers.

        Returns:
            list[CustomerResponseDTO]: List of all customers.
        """
        customers = self.repo.get_all()
        return [CustomerResponseDTO.model_validate(c) for c in customers]

    def update(self, customer_id: str, dto: UpdateCustomerDTO) -> CustomerResponseDTO | None:
        """Update an existing customer.

        Parameters:
            customer_id (str): The unique identifier of the customer.
            dto (UpdateCustomerDTO): Data transfer object containing
                updated customer data.

        Returns:
            CustomerResponseDTO | None: The updated customer response if
                found, None otherwise.
        """
        fields = dto.model_dump(exclude_none=True)
        updated = self.repo.update(customer_id, **fields)
        if updated is None:
            return None
        return CustomerResponseDTO.model_validate(updated)

    def delete(self, customer_id: str) -> bool:
        """Delete a customer.

        Parameters:
            customer_id (str): The unique identifier of the customer.

        Returns:
            bool: True if deletion was successful, False if customer
                not found.
        """
        return self.repo.delete(customer_id)
