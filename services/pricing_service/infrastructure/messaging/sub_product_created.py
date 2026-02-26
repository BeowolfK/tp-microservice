import json
from sqlalchemy.orm import Session
from services.pricing_service.infrastructure.db.schema import (
    PricingModel, engine,
)


def on_product_created(data: dict):
    product_pk = data.get("id")
    with Session(engine) as session:
        existing = session.query(PricingModel).filter_by(
            product_pk=product_pk
        ).first()
        if not existing:
            pricing = PricingModel(
                product_pk=product_pk, price=0.0,
            )
            session.add(pricing)
            session.commit()
