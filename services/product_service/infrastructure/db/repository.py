"""Repository pour l'acces aux donnees Product."""

from sqlalchemy.orm import Session
from .schema import ProductModel


class ProductRepository:
    """Repository CRUD pour les produits."""

    def __init__(self, session: Session) -> None:
        """Initialise le repository avec une session SQLAlchemy."""
        self.session = session

    def create(self, product: ProductModel) -> ProductModel:
        """Persiste un nouveau produit en base."""
        self.session.add(product)
        self.session.commit()
        self.session.refresh(product)
        return product

    def get(self, product_id: str) -> ProductModel | None:
        """Recupere un produit par son identifiant."""
        return self.session.get(ProductModel, product_id)

    def get_all(self) -> list[ProductModel]:
        """Recupere tous les produits."""
        return self.session.query(ProductModel).all()

    def update(self, product_id: str, **fields: object) -> ProductModel | None:
        """Met a jour les champs d'un produit existant."""
        product = self.get(product_id)
        if product is None:
            return None
        for key, value in fields.items():
            setattr(product, key, value)
        self.session.commit()
        self.session.refresh(product)
        return product

    def delete(self, product_id: str) -> bool:
        """Supprime un produit par son identifiant."""
        product = self.get(product_id)
        if product is None:
            return False
        self.session.delete(product)
        self.session.commit()
        return True
