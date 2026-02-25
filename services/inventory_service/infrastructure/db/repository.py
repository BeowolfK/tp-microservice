from sqlalchemy.orm import Session
from .schema import WarehouseModel, InventoryModel


class WarehouseRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, warehouse: WarehouseModel) -> WarehouseModel:
        self.session.add(warehouse)
        self.session.commit()
        self.session.refresh(warehouse)
        return warehouse

    def get(self, warehouse_id: str) -> WarehouseModel | None:
        return self.session.get(WarehouseModel, warehouse_id)

    def get_all(self) -> list[WarehouseModel]:
        return self.session.query(WarehouseModel).all()


class InventoryRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, item: InventoryModel) -> InventoryModel:
        self.session.add(item)
        self.session.commit()
        self.session.refresh(item)
        return item

    def get_by_product(self, product_pk: str) -> list[InventoryModel]:
        return self.session.query(InventoryModel).filter_by(product_pk=product_pk).all()

    def get_by_product_and_warehouse(self, product_pk: str, warehouse_pk: str) -> InventoryModel | None:
        return self.session.query(InventoryModel).filter_by(
            product_pk=product_pk, warehouse_pk=warehouse_pk
        ).first()

    def update(self, warehouse_pk: str, product_pk: str, **fields) -> InventoryModel | None:
        item = self.get_by_product_and_warehouse(product_pk, warehouse_pk)
        if item is None:
            return None
        for key, value in fields.items():
            setattr(item, key, value)
        self.session.commit()
        self.session.refresh(item)
        return item
