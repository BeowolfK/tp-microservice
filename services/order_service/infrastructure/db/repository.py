from sqlalchemy.orm import Session
from .schema import OrderModel, OrderLineModel


class OrderRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, order: OrderModel) -> OrderModel:
        self.session.add(order)
        self.session.commit()
        self.session.refresh(order)
        return order

    def get(self, order_id: str) -> OrderModel | None:
        return self.session.get(OrderModel, order_id)

    def get_all(self) -> list[OrderModel]:
        return self.session.query(OrderModel).all()

    def update(self, order_id: str, **fields) -> OrderModel | None:
        order = self.get(order_id)
        if order is None:
            return None
        for key, value in fields.items():
            setattr(order, key, value)
        self.session.commit()
        self.session.refresh(order)
        return order

    def delete(self, order_id: str) -> bool:
        order = self.get(order_id)
        if order is None:
            return False
        self.session.delete(order)
        self.session.commit()
        return True


class OrderLineRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, order_line: OrderLineModel) -> OrderLineModel:
        self.session.add(order_line)
        self.session.commit()
        self.session.refresh(order_line)
        return order_line

    def get(self, order_line_id: str) -> OrderLineModel | None:
        return self.session.get(OrderLineModel, order_line_id)

    def get_by_order(self, order_id: str) -> list[OrderLineModel]:
        return self.session.query(OrderLineModel).filter_by(order_pk=order_id).all()

    def delete(self, order_line_id: str) -> bool:
        order_line = self.get(order_line_id)
        if order_line is None:
            return False
        self.session.delete(order_line)
        self.session.commit()
        return True
