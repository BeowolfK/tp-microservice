from services.gateway_service.infrastructure.messaging.req_product import ProductClient


class ProductGatewayService:
    def __init__(self, client: ProductClient):
        self.client = client

    def create(self, data: dict) -> dict:
        return self.client.create(data)

    def get(self, product_id: str) -> dict:
        return self.client.get(product_id)

    def get_all(self) -> dict:
        return self.client.get_all()

    def update(self, product_id: str, data: dict) -> dict:
        return self.client.update(product_id, data)

    def delete(self, product_id: str) -> dict:
        return self.client.delete(product_id)
