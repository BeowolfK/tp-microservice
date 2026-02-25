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
    def __init__(self, session):
        self.warehouse_repo = WarehouseRepository(session)
        self.inventory_repo = InventoryRepository(session)

    def create_warehouse(self, dto: CreateWarehouseDTO) -> WarehouseResponseDTO:
        warehouse = WarehouseModel(
            name=dto.name,
            location=dto.location,
        )
        created = self.warehouse_repo.create(warehouse)
        return WarehouseResponseDTO.model_validate(created)

    def get_warehouse(self, warehouse_id: str) -> WarehouseResponseDTO | None:
        warehouse = self.warehouse_repo.get(warehouse_id)
        if warehouse is None:
            return None
        return WarehouseResponseDTO.model_validate(warehouse)

    def get_all_warehouses(self) -> list[WarehouseResponseDTO]:
        warehouses = self.warehouse_repo.get_all()
        return [WarehouseResponseDTO.model_validate(w) for w in warehouses]

    def create_inventory(self, dto: CreateInventoryDTO) -> InventoryResponseDTO:
        item = InventoryModel(
            product_pk=dto.product_pk,
            warehouse_pk=dto.warehouse_pk,
            quantity=dto.quantity,
        )
        created = self.inventory_repo.create(item)
        return InventoryResponseDTO.model_validate(created)

    def get_inventory_by_product(self, product_pk: str) -> list[InventoryResponseDTO]:
        items = self.inventory_repo.get_by_product(product_pk)
        return [InventoryResponseDTO.model_validate(i) for i in items]

    def update_inventory(self, warehouse_pk: str, product_pk: str, dto: UpdateInventoryDTO) -> InventoryResponseDTO | None:
        updated = self.inventory_repo.update(warehouse_pk, product_pk, quantity=dto.quantity)
        if updated is None:
            return None
        return InventoryResponseDTO.model_validate(updated)
