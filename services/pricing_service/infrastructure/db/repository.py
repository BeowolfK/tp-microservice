from sqlalchemy.orm import Session
from .schema import PricingModel


class PricingRepository:
    """Repository for managing pricing database operations.

    Provides data access layer for Pricing entities using SQLAlchemy.
    """
    def __init__(self, session: Session):
        """Initialize PricingRepository with a database session.

        Parameters:
            session (Session): SQLAlchemy database session.

        Returns:
            None
        """
        self.session = session

    def create(self, pricing: PricingModel) -> PricingModel:
        """Create and persist a new pricing entry.

        Parameters:
            pricing (PricingModel): Pricing model instance to create.

        Returns:
            PricingModel: The persisted pricing with generated ID.
        """
        self.session.add(pricing)
        self.session.commit()
        self.session.refresh(pricing)
        return pricing

    def get_by_product(self, product_pk: str) -> PricingModel | None:
        """Retrieve pricing for a product.

        Parameters:
            product_pk (str): The product primary key.

        Returns:
            PricingModel | None: The pricing if found, None otherwise.
        """
        return self.session.query(PricingModel).filter_by(product_pk=product_pk).first()

    def update_by_product(self, product_pk: str, **fields) -> PricingModel | None:
        """Update pricing for a product with provided field values.

        Parameters:
            product_pk (str): The product primary key.
            **fields: Keyword arguments of fields to update.

        Returns:
            PricingModel | None: The updated pricing if found,
                None otherwise.
        """
        pricing = self.get_by_product(product_pk)
        if pricing is None:
            return None
        for key, value in fields.items():
            setattr(pricing, key, value)
        self.session.commit()
        self.session.refresh(pricing)
        return pricing

    def delete_by_product(self, product_pk: str) -> bool:
        """Delete pricing for a product.

        Parameters:
            product_pk (str): The product primary key.

        Returns:
            bool: True if deletion was successful, False if pricing
                not found.
        """
        pricing = self.get_by_product(product_pk)
        if pricing is None:
            return False
        self.session.delete(pricing)
        self.session.commit()
        return True
