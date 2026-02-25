"""Publication d'evenements Product via ZeroMQ PUB."""

import json
import zmq


def publish_product_event(pub_socket: zmq.Socket, event: str, data: dict) -> None:
    """Publie un evenement produit sur le socket PUB."""
    payload: str = json.dumps(data)
    pub_socket.send_string(f"{event} {payload}")
