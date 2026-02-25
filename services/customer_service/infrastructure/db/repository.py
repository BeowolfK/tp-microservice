from sqlalchemy.orm import Session
from .schema import CustomerModel


class CustomerRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, customer: CustomerModel) -> CustomerModel:
        self.session.add(customer)
        self.session.commit()
        self.session.refresh(customer)
        return customer

    def get(self, customer_id: str) -> CustomerModel | None:
        return self.session.get(CustomerModel, customer_id)

    def get_all(self) -> list[CustomerModel]:
        return self.session.query(CustomerModel).all()

    def update(self, customer_id: str, **fields) -> CustomerModel | None:
        customer = self.get(customer_id)
        if customer is None:
            return None
        for key, value in fields.items():
            setattr(customer, key, value)
        self.session.commit()
        self.session.refresh(customer)
        return customer

    def delete(self, customer_id: str) -> bool:
        customer = self.get(customer_id)
        if customer is None:
            return False
        self.session.delete(customer)
        self.session.commit()
        return True
