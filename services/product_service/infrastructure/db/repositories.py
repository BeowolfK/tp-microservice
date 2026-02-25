from sqlalchemy.orm import Session

from .models import ProductModel


class ProductRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, product: ProductModel) -> ProductModel:
        self.session.add(product)
        self.session.commit()
        self.session.refresh(product)
        return product

    def get(self, product_id: str) -> ProductModel | None:
        return self.session.get(ProductModel, product_id)

    def get_all(self) -> list[ProductModel]:
        return self.session.query(ProductModel).all()

    def update(self, product_id: str, **fields) -> ProductModel | None:
        product = self.get(product_id)
        if product is None:
            return None
        for key, value in fields.items():
            setattr(product, key, value)
        self.session.commit()
        self.session.refresh(product)
        return product

    def delete(self, product_id: str) -> bool:
        product = self.get(product_id)
        if product is None:
            return False
        self.session.delete(product)
        self.session.commit()
        return True
