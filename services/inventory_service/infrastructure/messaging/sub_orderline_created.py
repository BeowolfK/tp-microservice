from sqlalchemy.orm import Session
from services.inventory_service.infrastructure.db.schema import (
    InventoryModel, engine,
)


def on_orderline_created(data: dict):
    """Decrement inventory when an orderline is created."""
    product_pk = data.get("product_pk")
    quantity = data.get("quantity", 1)
    warehouse_pk = data.get("warehouse_pk")
    with Session(engine) as session:
        if warehouse_pk:
            item = session.query(InventoryModel).filter_by(
                product_pk=product_pk,
                warehouse_pk=warehouse_pk,
            ).first()
        else:
            item = (
                session.query(InventoryModel)
                .filter(
                    InventoryModel.product_pk == product_pk,
                    InventoryModel.quantity >= quantity,
                )
                .first()
            )
        if item and item.quantity >= quantity:
            item.quantity -= quantity
            session.commit()
