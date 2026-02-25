from services.order_service.infrastructure.db.schema import OrderModel, OrderLineModel
from services.order_service.infrastructure.db.repository import OrderRepository
from services.order_service.application.dtos import (
    CreateOrderDTO,
    UpdateOrderDTO,
    OrderResponseDTO,
    OrderLineResponseDTO,
)


class OrderService:
    def __init__(self, session):
        self.repo = OrderRepository(session)

    def create(self, dto: CreateOrderDTO) -> OrderResponseDTO:
        order = OrderModel(
            customer_pk=dto.customer_pk,
            status="pending",
        )
        for line_dto in dto.lines:
            order_line = OrderLineModel(
                product_pk=line_dto.product_pk,
                quantity=line_dto.quantity,
                unit_price=line_dto.unit_price,
            )
            order.lines.append(order_line)
        created = self.repo.create(order)
        return self._to_response(created)

    def get(self, order_id: str) -> OrderResponseDTO | None:
        order = self.repo.get(order_id)
        if order is None:
            return None
        return self._to_response(order)

    def update_status(self, order_id: str, dto: UpdateOrderDTO) -> OrderResponseDTO | None:
        fields = dto.model_dump(exclude_none=True)
        updated = self.repo.update(order_id, **fields)
        if updated is None:
            return None
        return self._to_response(updated)

    def _to_response(self, order: OrderModel) -> OrderResponseDTO:
        lines = [
            OrderLineResponseDTO(
                id=str(line.id),
                order_pk=str(line.order_pk),
                product_pk=str(line.product_pk),
                quantity=line.quantity,
                unit_price=line.unit_price,
            )
            for line in order.lines
        ]
        return OrderResponseDTO(
            id=str(order.id),
            customer_pk=str(order.customer_pk),
            status=str(order.status),
            created_at=order.created_at.isoformat(),
            lines=lines,
        )
