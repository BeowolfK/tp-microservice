"""Point d'entree du microservice Product (ZeroMQ REP:5555 + PUB:5560)."""

import json
import zmq
from sqlalchemy.orm import Session

from services.product_service.infrastructure.db.schema import Base, engine
from services.product_service.application.dtos import (
    CreateProductDTO, UpdateProductDTO,
)
from services.product_service.application.services.crud_service import (
    ProductService,
)
from services.product_service.domain.events import PRODUCT_CREATED

Base.metadata.create_all(engine)

pub_socket: zmq.Socket | None = None


def handle_request(message: dict) -> dict:
    """Traite une requete REQ/REP et retourne la reponse JSON."""
    action: str | None = message.get("action")
    data: dict = message.get("data", {})

    with Session(engine) as session:
        service = ProductService(session)
        response: dict = {"success": True, "data": None}

        try:
            if action == "create":
                dto = CreateProductDTO(**data)
                result = service.create(dto)
                response["data"] = result.model_dump()
                if pub_socket:
                    payload = json.dumps(response["data"])
                    pub_socket.send_string(
                        f"{PRODUCT_CREATED} {payload}"
                    )

            elif action == "get":
                result = service.get(data["id"])
                if result is None:
                    response = {
                        "success": False,
                        "error": "Produit non trouve",
                    }
                else:
                    response["data"] = result.model_dump()

            elif action == "get_all":
                results = service.get_all()
                response["data"] = [
                    r.model_dump() for r in results
                ]

            elif action == "update":
                product_id = data.pop("id")
                dto = UpdateProductDTO(**data)
                result = service.update(product_id, dto)
                if result is None:
                    response = {
                        "success": False,
                        "error": "Produit non trouve",
                    }
                else:
                    response["data"] = result.model_dump()

            elif action == "delete":
                deleted = service.delete(data["id"])
                if not deleted:
                    response = {
                        "success": False,
                        "error": "Produit non trouve",
                    }

            else:
                response = {
                    "success": False,
                    "error": f"Action inconnue: {action}",
                }

        except Exception as e:
            response = {"success": False, "error": str(e)}

    return response


def main() -> None:
    """Demarre le service Product avec les sockets ZeroMQ."""
    global pub_socket
    print("[product-service] Demarrage...")
    ctx = zmq.Context()

    rep = ctx.socket(zmq.REP)
    rep.bind("tcp://0.0.0.0:5555")

    pub_socket = ctx.socket(zmq.PUB)
    pub_socket.bind("tcp://0.0.0.0:5560")

    pair_pricing = ctx.socket(zmq.PAIR)
    pair_pricing.connect("tcp://pricing-service:5563")

    pair_inventory = ctx.socket(zmq.PAIR)
    pair_inventory.connect("tcp://inventory-service:5564")

    print("[product-service] REP:5555 PUB:5560 ready")

    while True:
        message = rep.recv_json()
        response = handle_request(message)
        rep.send_json(response)


if __name__ == "__main__":
    main()
