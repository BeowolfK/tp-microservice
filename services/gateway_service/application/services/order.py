from services.gateway_service.infrastructure.messaging.req_order import OrderClient


class OrderGatewayService:
    def __init__(self, client: OrderClient):
        self.client = client

    def create(self, data: dict) -> dict:
        return self.client.create(data)

    def get(self, order_id: str) -> dict:
        return self.client.get(order_id)

    def update(self, order_id: str, data: dict) -> dict:
        return self.client.update(order_id, data)
