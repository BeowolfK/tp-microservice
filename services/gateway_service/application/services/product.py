from services.gateway_service.infrastructure.messaging.req_product import ProductClient


class ProductGatewayService:
    """Gateway service for product operations.

    Acts as a proxy to the product service client for API requests
    from the gateway.
    """
    def __init__(self, client: ProductClient):
        """Initialize ProductGatewayService with a client.

        Parameters:
            client (ProductClient): The product service client.

        Returns:
            None
        """
        self.client = client

    def create(self, data: dict) -> dict:
        """Create a new product through the gateway.

        Parameters:
            data (dict): Product data for creation.

        Returns:
            dict: Response from the product service.
        """
        return self.client.create(data)

    def get(self, product_id: str) -> dict:
        """Retrieve a product by ID through the gateway.

        Parameters:
            product_id (str): The unique identifier of the product.

        Returns:
            dict: Response from the product service.
        """
        return self.client.get(product_id)

    def get_all(self) -> dict:
        """Retrieve all products through the gateway.

        Returns:
            dict: Response from the product service.
        """
        return self.client.get_all()

    def update(self, product_id: str, data: dict) -> dict:
        """Update a product through the gateway.

        Parameters:
            product_id (str): The unique identifier of the product.
            data (dict): Updated product data.

        Returns:
            dict: Response from the product service.
        """
        return self.client.update(product_id, data)

    def delete(self, product_id: str) -> dict:
        """Delete a product through the gateway.

        Parameters:
            product_id (str): The unique identifier of the product.

        Returns:
            dict: Response from the product service.
        """
        return self.client.delete(product_id)
