from sqlalchemy.orm import Session
from .schema import OrderModel, OrderLineModel


class OrderRepository:
    """Repository for managing order database operations.

    Provides data access layer for Order entities using SQLAlchemy.
    """
    def __init__(self, session: Session):
        """Initialize OrderRepository with a database session.

        Parameters:
            session (Session): SQLAlchemy database session.

        Returns:
            None
        """
        self.session = session

    def create(self, order: OrderModel) -> OrderModel:
        """Create and persist a new order.

        Parameters:
            order (OrderModel): Order model instance to create.

        Returns:
            OrderModel: The persisted order with generated ID.
        """
        self.session.add(order)
        self.session.commit()
        self.session.refresh(order)
        return order

    def get(self, order_id: str) -> OrderModel | None:
        """Retrieve an order by ID.

        Parameters:
            order_id (str): The unique identifier of the order.

        Returns:
            OrderModel | None: The order if found, None otherwise.
        """
        return self.session.get(OrderModel, order_id)

    def get_all(self) -> list[OrderModel]:
        """Retrieve all orders.

        Returns:
            list[OrderModel]: List of all order records.
        """
        return self.session.query(OrderModel).all()

    def update(self, order_id: str, **fields) -> OrderModel | None:
        """Update an order with provided field values.

        Parameters:
            order_id (str): The unique identifier of the order.
            **fields: Keyword arguments of fields to update.

        Returns:
            OrderModel | None: The updated order if found,
                None otherwise.
        """
        order = self.get(order_id)
        if order is None:
            return None
        for key, value in fields.items():
            setattr(order, key, value)
        self.session.commit()
        self.session.refresh(order)
        return order

    def delete(self, order_id: str) -> bool:
        """Delete an order.

        Parameters:
            order_id (str): The unique identifier of the order.

        Returns:
            bool: True if deletion was successful, False if order
                not found.
        """
        order = self.get(order_id)
        if order is None:
            return False
        self.session.delete(order)
        self.session.commit()
        return True


class OrderLineRepository:
    """Repository for managing order line database operations.

    Provides data access layer for OrderLine entities using SQLAlchemy.
    """
    def __init__(self, session: Session):
        """Initialize OrderLineRepository with a database session.

        Parameters:
            session (Session): SQLAlchemy database session.

        Returns:
            None
        """
        self.session = session

    def create(self, order_line: OrderLineModel) -> OrderLineModel:
        """Create and persist a new order line.

        Parameters:
            order_line (OrderLineModel): Order line model instance to create.

        Returns:
            OrderLineModel: The persisted order line with generated ID.
        """
        self.session.add(order_line)
        self.session.commit()
        self.session.refresh(order_line)
        return order_line

    def get(self, order_line_id: str) -> OrderLineModel | None:
        """Retrieve an order line by ID.

        Parameters:
            order_line_id (str): The unique identifier of the order line.

        Returns:
            OrderLineModel | None: The order line if found, None otherwise.
        """
        return self.session.get(OrderLineModel, order_line_id)

    def get_by_order(self, order_id: str) -> list[OrderLineModel]:
        """Retrieve all line items for an order.

        Parameters:
            order_id (str): The unique identifier of the order.

        Returns:
            list[OrderLineModel]: List of order line records for the order.
        """
        return self.session.query(OrderLineModel).filter_by(order_pk=order_id).all()

    def delete(self, order_line_id: str) -> bool:
        """Delete an order line.

        Parameters:
            order_line_id (str): The unique identifier of the order line.

        Returns:
            bool: True if deletion was successful, False if order line
                not found.
        """
        order_line = self.get(order_line_id)
        if order_line is None:
            return False
        self.session.delete(order_line)
        self.session.commit()
        return True
