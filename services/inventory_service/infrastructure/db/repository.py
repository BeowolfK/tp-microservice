from sqlalchemy.orm import Session
from .schema import WarehouseModel, InventoryModel


class WarehouseRepository:
    """Repository for managing warehouse database operations.

    Provides data access layer for Warehouse entities using SQLAlchemy.
    """
    def __init__(self, session: Session):
        """Initialize WarehouseRepository with a database session.

        Parameters:
            session (Session): SQLAlchemy database session.

        Returns:
            None
        """
        self.session = session

    def create(self, warehouse: WarehouseModel) -> WarehouseModel:
        """Create and persist a new warehouse.

        Parameters:
            warehouse (WarehouseModel): Warehouse model instance to create.

        Returns:
            WarehouseModel: The persisted warehouse with generated ID.
        """
        self.session.add(warehouse)
        self.session.commit()
        self.session.refresh(warehouse)
        return warehouse

    def get(self, warehouse_id: str) -> WarehouseModel | None:
        """Retrieve a warehouse by ID.

        Parameters:
            warehouse_id (str): The unique identifier of the warehouse.

        Returns:
            WarehouseModel | None: The warehouse if found, None otherwise.
        """
        return self.session.get(WarehouseModel, warehouse_id)

    def get_all(self) -> list[WarehouseModel]:
        """Retrieve all warehouses.

        Returns:
            list[WarehouseModel]: List of all warehouse records.
        """
        return self.session.query(WarehouseModel).all()


class InventoryRepository:
    """Repository for managing inventory database operations.

    Provides data access layer for InventoryItem entities using SQLAlchemy.
    """
    def __init__(self, session: Session):
        """Initialize InventoryRepository with a database session.

        Parameters:
            session (Session): SQLAlchemy database session.

        Returns:
            None
        """
        self.session = session

    def create(self, item: InventoryModel) -> InventoryModel:
        """Create and persist a new inventory item.

        Parameters:
            item (InventoryModel): Inventory model instance to create.

        Returns:
            InventoryModel: The persisted inventory with generated ID.
        """
        self.session.add(item)
        self.session.commit()
        self.session.refresh(item)
        return item

    def get_by_product(self, product_pk: str) -> list[InventoryModel]:
        """Retrieve all inventory items for a product.

        Parameters:
            product_pk (str): The product primary key.

        Returns:
            list[InventoryModel]: List of inventory items for the product.
        """
        return self.session.query(InventoryModel).filter_by(product_pk=product_pk).all()

    def get_by_product_and_warehouse(self, product_pk: str, warehouse_pk: str) -> InventoryModel | None:
        """Retrieve inventory for a specific product and warehouse.

        Parameters:
            product_pk (str): The product primary key.
            warehouse_pk (str): The warehouse primary key.

        Returns:
            InventoryModel | None: The inventory item if found,
                None otherwise.
        """
        return self.session.query(InventoryModel).filter_by(
            product_pk=product_pk, warehouse_pk=warehouse_pk
        ).first()

    def update(self, warehouse_pk: str, product_pk: str, **fields) -> InventoryModel | None:
        """Update inventory item with provided field values.

        Parameters:
            warehouse_pk (str): The warehouse primary key.
            product_pk (str): The product primary key.
            **fields: Keyword arguments of fields to update.

        Returns:
            InventoryModel | None: The updated inventory if found,
                None otherwise.
        """
        item = self.get_by_product_and_warehouse(product_pk, warehouse_pk)
        if item is None:
            return None
        for key, value in fields.items():
            setattr(item, key, value)
        self.session.commit()
        self.session.refresh(item)
        return item
