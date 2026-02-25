from services.gateway_service.infrastructure.messaging.req_inventory import InventoryClient


class InventoryGatewayService:
    def __init__(self, client: InventoryClient):
        self.client = client

    def create_warehouse(self, data: dict) -> dict:
        return self.client.create_warehouse(data)

    def get_warehouse(self, warehouse_id: str) -> dict:
        return self.client.get_warehouse(warehouse_id)

    def get_all_warehouses(self) -> dict:
        return self.client.get_all_warehouses()

    def create_inventory(self, data: dict) -> dict:
        return self.client.create_inventory(data)

    def get_by_product(self, product_pk: str) -> dict:
        return self.client.get_by_product(product_pk)

    def update(self, warehouse_pk: str, product_pk: str, quantity: int) -> dict:
        return self.client.update(warehouse_pk, product_pk, quantity)
