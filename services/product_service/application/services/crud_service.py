"""Service applicatif CRUD pour les produits."""

from sqlalchemy.orm import Session

from services.product_service.infrastructure.db.schema import ProductModel
from services.product_service.infrastructure.db.repository import ProductRepository
from services.product_service.application.dtos import (
    CreateProductDTO,
    UpdateProductDTO,
    ProductResponseDTO,
)


class ProductService:
    """Service CRUD pour la gestion des produits."""

    def __init__(self, session: Session) -> None:
        """Initialise le service avec une session SQLAlchemy."""
        self.repo = ProductRepository(session)

    def create(self, dto: CreateProductDTO) -> ProductResponseDTO:
        """Cree un nouveau produit a partir du DTO."""
        product = ProductModel(
            name=dto.name,
            description=dto.description,
            category=dto.category,
            available=dto.available,
        )
        created = self.repo.create(product)
        return ProductResponseDTO.model_validate(created)

    def get(self, product_id: str) -> ProductResponseDTO | None:
        """Recupere un produit par son identifiant."""
        product = self.repo.get(product_id)
        if product is None:
            return None
        return ProductResponseDTO.model_validate(product)

    def get_all(self) -> list[ProductResponseDTO]:
        """Recupere tous les produits."""
        products = self.repo.get_all()
        return [ProductResponseDTO.model_validate(p) for p in products]

    def update(self, product_id: str, dto: UpdateProductDTO) -> ProductResponseDTO | None:
        """Met a jour un produit existant."""
        fields = dto.model_dump(exclude_none=True)
        updated = self.repo.update(product_id, **fields)
        if updated is None:
            return None
        return ProductResponseDTO.model_validate(updated)

    def delete(self, product_id: str) -> bool:
        """Supprime un produit par son identifiant."""
        return self.repo.delete(product_id)
