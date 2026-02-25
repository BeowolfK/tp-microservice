from sqlalchemy.orm import Session
from services.inventory_service.infrastructure.db.schema import (
    WarehouseModel, InventoryModel, engine,
)


def on_product_created(data: dict):
    """Create inventory entries (qty=0) for all warehouses."""
    product_pk = data.get("id")
    with Session(engine) as session:
        warehouses = session.query(WarehouseModel).all()
        for wh in warehouses:
            existing = session.query(InventoryModel).filter_by(
                product_pk=product_pk, warehouse_pk=wh.id,
            ).first()
            if not existing:
                item = InventoryModel(
                    product_pk=product_pk,
                    warehouse_pk=wh.id,
                    quantity=0,
                )
                session.add(item)
        session.commit()
