from services.inventory_service.infrastructure.db.schema import WarehouseModel, InventoryModel
from services.inventory_service.infrastructure.db.repository import WarehouseRepository, InventoryRepository
from services.inventory_service.application.dtos import (
    CreateWarehouseDTO,
    WarehouseResponseDTO,
    CreateInventoryDTO,
    UpdateInventoryDTO,
    InventoryResponseDTO,
)


class InventoryService:
    """Service layer for managing warehouse and inventory operations.

    Handles business logic for warehouse and inventory CRUD operations
    using the warehouse and inventory repositories.
    """
    def __init__(self, session):
        """Initialize InventoryService with a database session.

        Parameters:
            session: SQLAlchemy database session.

        Returns:
            None
        """
        self.warehouse_repo = WarehouseRepository(session)
        self.inventory_repo = InventoryRepository(session)

    def create_warehouse(self, dto: CreateWarehouseDTO) -> WarehouseResponseDTO:
        """Create a new warehouse.

        Parameters:
            dto (CreateWarehouseDTO): Data transfer object containing
                warehouse creation data.

        Returns:
            WarehouseResponseDTO: The created warehouse response.
        """
        warehouse = WarehouseModel(
            name=dto.name,
            location=dto.location,
        )
        created = self.warehouse_repo.create(warehouse)
        return WarehouseResponseDTO.model_validate(created)

    def get_warehouse(self, warehouse_id: str) -> WarehouseResponseDTO | None:
        """Retrieve a warehouse by ID.

        Parameters:
            warehouse_id (str): The unique identifier of the warehouse.

        Returns:
            WarehouseResponseDTO | None: The warehouse response if found,
                None otherwise.
        """
        warehouse = self.warehouse_repo.get(warehouse_id)
        if warehouse is None:
            return None
        return WarehouseResponseDTO.model_validate(warehouse)

    def get_all_warehouses(self) -> list[WarehouseResponseDTO]:
        """Retrieve all warehouses.

        Returns:
            list[WarehouseResponseDTO]: List of all warehouses.
        """
        warehouses = self.warehouse_repo.get_all()
        return [WarehouseResponseDTO.model_validate(w) for w in warehouses]

    def create_inventory(self, dto: CreateInventoryDTO) -> InventoryResponseDTO:
        """Create a new inventory item.

        Parameters:
            dto (CreateInventoryDTO): Data transfer object containing
                inventory creation data.

        Returns:
            InventoryResponseDTO: The created inventory response.
        """
        item = InventoryModel(
            product_pk=dto.product_pk,
            warehouse_pk=dto.warehouse_pk,
            quantity=dto.quantity,
        )
        created = self.inventory_repo.create(item)
        return InventoryResponseDTO.model_validate(created)

    def get_inventory_by_product(self, product_pk: str) -> list[InventoryResponseDTO]:
        """Retrieve all inventory items for a product.

        Parameters:
            product_pk (str): The product primary key.

        Returns:
            list[InventoryResponseDTO]: List of inventory items for
                the product.
        """
        items = self.inventory_repo.get_by_product(product_pk)
        return [InventoryResponseDTO.model_validate(i) for i in items]

    def update_inventory(self, warehouse_pk: str, product_pk: str, dto: UpdateInventoryDTO) -> InventoryResponseDTO | None:
        """Update inventory quantity for a product in a warehouse.

        Parameters:
            warehouse_pk (str): The warehouse primary key.
            product_pk (str): The product primary key.
            dto (UpdateInventoryDTO): Data transfer object containing
                updated quantity.

        Returns:
            InventoryResponseDTO | None: The updated inventory response
                if found, None otherwise.
        """
        updated = self.inventory_repo.update(warehouse_pk, product_pk, quantity=dto.quantity)
        if updated is None:
            return None
        return InventoryResponseDTO.model_validate(updated)
