"""Client PAIR ZeroMQ pour communiquer avec le service Pricing."""

import zmq


class PricingPairClient:
    """Client PAIR pour recuperer le prix d'un produit."""

    def __init__(self, socket: zmq.Socket) -> None:
        """Initialise le client avec un socket PAIR connecte."""
        self.socket = socket

    def get_price(self, product_id: str) -> dict:
        """Demande le prix d'un produit au service Pricing."""
        self.socket.send_json({
            "action": "get_price",
            "product_pk": product_id,
        })
        return self.socket.recv_json()
