"""Client PAIR ZeroMQ pour communiquer avec le service Inventory."""

import zmq


class InventoryPairClient:
    """Client PAIR pour recuperer la quantite en stock d'un produit."""

    def __init__(self, socket: zmq.Socket) -> None:
        """Initialise le client avec un socket PAIR connecte."""
        self.socket = socket

    def get_inventory(self, product_id: str) -> dict:
        """Demande la quantite en stock d'un produit au service Inventory."""
        self.socket.send_json({
            "action": "get_nb_in_inventory",
            "product_pk": product_id,
        })
        return self.socket.recv_json()
