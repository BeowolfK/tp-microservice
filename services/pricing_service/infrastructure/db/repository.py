from sqlalchemy.orm import Session
from .schema import PricingModel


class PricingRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, pricing: PricingModel) -> PricingModel:
        self.session.add(pricing)
        self.session.commit()
        self.session.refresh(pricing)
        return pricing

    def get_by_product(self, product_pk: str) -> PricingModel | None:
        return self.session.query(PricingModel).filter_by(product_pk=product_pk).first()

    def update_by_product(self, product_pk: str, **fields) -> PricingModel | None:
        pricing = self.get_by_product(product_pk)
        if pricing is None:
            return None
        for key, value in fields.items():
            setattr(pricing, key, value)
        self.session.commit()
        self.session.refresh(pricing)
        return pricing

    def delete_by_product(self, product_pk: str) -> bool:
        pricing = self.get_by_product(product_pk)
        if pricing is None:
            return False
        self.session.delete(pricing)
        self.session.commit()
        return True
