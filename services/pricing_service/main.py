import json
import threading
import zmq
from sqlalchemy.orm import Session

from services.pricing_service.infrastructure.db.schema import (
    Base, engine, PricingModel,
)
from services.pricing_service.application.dtos import (
    CreatePricingDTO, UpdatePricingDTO,
)
from services.pricing_service.application.services.crud_service import (
    PricingService,
)
from services.pricing_service.infrastructure.messaging.sub_product_created import (
    on_product_created,
)

Base.metadata.create_all(engine)


def handle_request(message: dict) -> dict:
    action = message.get("action")
    data = message.get("data", {})

    with Session(engine) as session:
        service = PricingService(session)
        response = {"success": True, "data": None}

        try:
            if action == "create":
                dto = CreatePricingDTO(**data)
                result = service.create(dto)
                response["data"] = result.model_dump()

            elif action == "get":
                result = service.get_by_product(data["product_pk"])
                if result is None:
                    response = {
                        "success": False,
                        "error": "Non trouve",
                    }
                else:
                    response["data"] = result.model_dump()

            elif action == "update":
                dto = UpdatePricingDTO(price=data["price"])
                result = service.update_by_product(
                    data["product_pk"], dto,
                )
                if result is None:
                    response = {
                        "success": False,
                        "error": "Non trouve",
                    }
                else:
                    response["data"] = result.model_dump()

            elif action == "delete":
                deleted = service.delete(data["product_pk"])
                if not deleted:
                    response = {
                        "success": False,
                        "error": "Non trouve",
                    }

            else:
                response = {
                    "success": False,
                    "error": f"Action inconnue: {action}",
                }

        except Exception as e:
            response = {"success": False, "error": str(e)}

    return response


def handle_pair(pair_socket):
    """Handle PAIR requests from product-service."""
    while True:
        msg = pair_socket.recv_json()
        action = msg.get("action")
        product_pk = msg.get("product_pk")
        if action == "get_price":
            with Session(engine) as session:
                pricing = session.query(PricingModel).filter_by(
                    product_pk=product_pk
                ).first()
                if pricing:
                    pair_socket.send_json({
                        "price": pricing.price,
                    })
                else:
                    pair_socket.send_json({"price": None})
        else:
            pair_socket.send_json({"error": "unknown"})


def sub_product_events(ctx):
    """SUB thread: listen for product.created events."""
    sub = ctx.socket(zmq.SUB)
    sub.connect("tcp://product-service:5560")
    sub.subscribe(b"product.created")

    while True:
        msg = sub.recv_string()
        topic, payload = msg.split(" ", 1)
        data = json.loads(payload)
        on_product_created(data)


def main():
    print("[pricing-service] Demarrage...")
    ctx = zmq.Context()

    rep = ctx.socket(zmq.REP)
    rep.bind("tcp://0.0.0.0:5558")

    pair = ctx.socket(zmq.PAIR)
    pair.bind("tcp://0.0.0.0:5563")

    # Background threads
    threading.Thread(
        target=handle_pair, args=(pair,), daemon=True,
    ).start()
    threading.Thread(
        target=sub_product_events, args=(ctx,), daemon=True,
    ).start()

    print("[pricing-service] REP:5558 PAIR:5563 ready")

    while True:
        message = rep.recv_json()
        response = handle_request(message)
        rep.send_json(response)


if __name__ == "__main__":
    main()
