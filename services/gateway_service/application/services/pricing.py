from services.gateway_service.infrastructure.messaging.req_pricing import PricingClient


class PricingGatewayService:
    def __init__(self, client: PricingClient):
        self.client = client

    def create(self, data: dict) -> dict:
        return self.client.create(data)

    def get(self, product_pk: str) -> dict:
        return self.client.get(product_pk)

    def update(self, product_pk: str, price: float) -> dict:
        return self.client.update(product_pk, price)
