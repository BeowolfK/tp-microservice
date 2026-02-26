from services.gateway_service.infrastructure.messaging.req_pricing import PricingClient


class PricingGatewayService:
    """Gateway service for pricing operations.

    Acts as a proxy to the pricing service client for API requests
    from the gateway.
    """
    def __init__(self, client: PricingClient):
        """Initialize PricingGatewayService with a client.

        Parameters:
            client (PricingClient): The pricing service client.

        Returns:
            None
        """
        self.client = client

    def create(self, data: dict) -> dict:
        """Create new pricing through the gateway.

        Parameters:
            data (dict): Pricing data for creation.

        Returns:
            dict: Response from the pricing service.
        """
        return self.client.create(data)

    def get(self, product_pk: str) -> dict:
        """Retrieve pricing for a product through the gateway.

        Parameters:
            product_pk (str): The product primary key.

        Returns:
            dict: Response from the pricing service.
        """
        return self.client.get(product_pk)

    def update(self, product_pk: str, price: float) -> dict:
        """Update pricing for a product through the gateway.

        Parameters:
            product_pk (str): The product primary key.
            price (float): The new price.

        Returns:
            dict: Response from the pricing service.
        """
        return self.client.update(product_pk, price)
