from sqlalchemy.orm import Session
from .schema import CustomerModel


class CustomerRepository:
    """Repository for managing customer database operations.

    Provides data access layer for Customer entities using SQLAlchemy.
    """
    def __init__(self, session: Session):
        """Initialize CustomerRepository with a database session.

        Parameters:
            session (Session): SQLAlchemy database session.

        Returns:
            None
        """
        self.session = session

    def create(self, customer: CustomerModel) -> CustomerModel:
        """Create and persist a new customer.

        Parameters:
            customer (CustomerModel): Customer model instance to create.

        Returns:
            CustomerModel: The persisted customer with generated ID.
        """
        self.session.add(customer)
        self.session.commit()
        self.session.refresh(customer)
        return customer

    def get(self, customer_id: str) -> CustomerModel | None:
        """Retrieve a customer by ID.

        Parameters:
            customer_id (str): The unique identifier of the customer.

        Returns:
            CustomerModel | None: The customer if found, None otherwise.
        """
        return self.session.get(CustomerModel, customer_id)

    def get_all(self) -> list[CustomerModel]:
        """Retrieve all customers.

        Returns:
            list[CustomerModel]: List of all customer records.
        """
        return self.session.query(CustomerModel).all()

    def update(self, customer_id: str, **fields) -> CustomerModel | None:
        """Update a customer with provided field values.

        Parameters:
            customer_id (str): The unique identifier of the customer.
            **fields: Keyword arguments of fields to update.

        Returns:
            CustomerModel | None: The updated customer if found,
                None otherwise.
        """
        customer = self.get(customer_id)
        if customer is None:
            return None
        for key, value in fields.items():
            setattr(customer, key, value)
        self.session.commit()
        self.session.refresh(customer)
        return customer

    def delete(self, customer_id: str) -> bool:
        """Delete a customer.

        Parameters:
            customer_id (str): The unique identifier of the customer.

        Returns:
            bool: True if deletion was successful, False if customer
                not found.
        """
        customer = self.get(customer_id)
        if customer is None:
            return False
        self.session.delete(customer)
        self.session.commit()
        return True
