from services.gateway_service.infrastructure.messaging.req_inventory import InventoryClient


class InventoryGatewayService:
    """Gateway service for inventory operations.

    Acts as a proxy to the inventory service client for API requests
    from the gateway.
    """
    def __init__(self, client: InventoryClient):
        """Initialize InventoryGatewayService with a client.

        Parameters:
            client (InventoryClient): The inventory service client.

        Returns:
            None
        """
        self.client = client

    def create_warehouse(self, data: dict) -> dict:
        """Create a new warehouse through the gateway.

        Parameters:
            data (dict): Warehouse data for creation.

        Returns:
            dict: Response from the inventory service.
        """
        return self.client.create_warehouse(data)

    def get_warehouse(self, warehouse_id: str) -> dict:
        """Retrieve a warehouse by ID through the gateway.

        Parameters:
            warehouse_id (str): The unique identifier of the warehouse.

        Returns:
            dict: Response from the inventory service.
        """
        return self.client.get_warehouse(warehouse_id)

    def get_all_warehouses(self) -> dict:
        """Retrieve all warehouses through the gateway.

        Returns:
            dict: Response from the inventory service.
        """
        return self.client.get_all_warehouses()

    def create_inventory(self, data: dict) -> dict:
        """Create a new inventory item through the gateway.

        Parameters:
            data (dict): Inventory data for creation.

        Returns:
            dict: Response from the inventory service.
        """
        return self.client.create_inventory(data)

    def get_by_product(self, product_pk: str) -> dict:
        """Retrieve inventory for a product through the gateway.

        Parameters:
            product_pk (str): The product primary key.

        Returns:
            dict: Response from the inventory service.
        """
        return self.client.get_by_product(product_pk)

    def update(self, warehouse_pk: str, product_pk: str, quantity: int) -> dict:
        """Update inventory quantity through the gateway.

        Parameters:
            warehouse_pk (str): The warehouse primary key.
            product_pk (str): The product primary key.
            quantity (int): The new quantity.

        Returns:
            dict: Response from the inventory service.
        """
        return self.client.update(warehouse_pk, product_pk, quantity)
