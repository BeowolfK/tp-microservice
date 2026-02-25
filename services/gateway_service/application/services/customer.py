from services.gateway_service.infrastructure.messaging.req_customer import CustomerClient


class CustomerGatewayService:
    def __init__(self, client: CustomerClient):
        self.client = client

    def create(self, data: dict) -> dict:
        return self.client.create(data)

    def get(self, customer_id: str) -> dict:
        return self.client.get(customer_id)

    def get_all(self) -> dict:
        return self.client.get_all()

    def update(self, customer_id: str, data: dict) -> dict:
        return self.client.update(customer_id, data)

    def delete(self, customer_id: str) -> dict:
        return self.client.delete(customer_id)
