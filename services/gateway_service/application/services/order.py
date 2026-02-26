from services.gateway_service.infrastructure.messaging.req_order import OrderClient


class OrderGatewayService:
    """Gateway service for order operations.

    Acts as a proxy to the order service client for API requests
    from the gateway.
    """
    def __init__(self, client: OrderClient):
        """Initialize OrderGatewayService with a client.

        Parameters:
            client (OrderClient): The order service client.

        Returns:
            None
        """
        self.client = client

    def create(self, data: dict) -> dict:
        """Create a new order through the gateway.

        Parameters:
            data (dict): Order data for creation.

        Returns:
            dict: Response from the order service.
        """
        return self.client.create(data)

    def get(self, order_id: str) -> dict:
        """Retrieve an order by ID through the gateway.

        Parameters:
            order_id (str): The unique identifier of the order.

        Returns:
            dict: Response from the order service.
        """
        return self.client.get(order_id)

    def update(self, order_id: str, data: dict) -> dict:
        """Update an order through the gateway.

        Parameters:
            order_id (str): The unique identifier of the order.
            data (dict): Updated order data.

        Returns:
            dict: Response from the order service.
        """
        return self.client.update(order_id, data)
