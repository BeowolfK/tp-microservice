from services.gateway_service.infrastructure.messaging.req_customer import CustomerClient


class CustomerGatewayService:
    """Gateway service for customer operations.

    Acts as a proxy to the customer service client for API requests
    from the gateway.
    """
    def __init__(self, client: CustomerClient):
        """Initialize CustomerGatewayService with a client.

        Parameters:
            client (CustomerClient): The customer service client.

        Returns:
            None
        """
        self.client = client

    def create(self, data: dict) -> dict:
        """Create a new customer through the gateway.

        Parameters:
            data (dict): Customer data for creation.

        Returns:
            dict: Response from the customer service.
        """
        return self.client.create(data)

    def get(self, customer_id: str) -> dict:
        """Retrieve a customer by ID through the gateway.

        Parameters:
            customer_id (str): The unique identifier of the customer.

        Returns:
            dict: Response from the customer service.
        """
        return self.client.get(customer_id)

    def get_all(self) -> dict:
        """Retrieve all customers through the gateway.

        Returns:
            dict: Response from the customer service.
        """
        return self.client.get_all()

    def update(self, customer_id: str, data: dict) -> dict:
        """Update a customer through the gateway.

        Parameters:
            customer_id (str): The unique identifier of the customer.
            data (dict): Updated customer data.

        Returns:
            dict: Response from the customer service.
        """
        return self.client.update(customer_id, data)

    def delete(self, customer_id: str) -> dict:
        """Delete a customer through the gateway.

        Parameters:
            customer_id (str): The unique identifier of the customer.

        Returns:
            dict: Response from the customer service.
        """
        return self.client.delete(customer_id)
