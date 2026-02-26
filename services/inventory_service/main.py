import json
import threading
import zmq
from sqlalchemy.orm import Session

from services.inventory_service.infrastructure.db.schema import (
    Base, engine, InventoryModel,
)
from services.inventory_service.application.dtos import (
    CreateWarehouseDTO, CreateInventoryDTO, UpdateInventoryDTO,
)
from services.inventory_service.application.services.crud_service import (
    InventoryService,
)
from services.inventory_service.infrastructure.messaging.sub_product_created import (
    on_product_created,
)
from services.inventory_service.infrastructure.messaging.sub_orderline_created import (
    on_orderline_created,
)

Base.metadata.create_all(engine)


def handle_request(message: dict) -> dict:
    action = message.get("action")
    data = message.get("data", {})

    with Session(engine) as session:
        service = InventoryService(session)
        response = {"success": True, "data": None}

        try:
            if action == "create_warehouse":
                dto = CreateWarehouseDTO(**data)
                result = service.create_warehouse(dto)
                response["data"] = result.model_dump()

            elif action == "get_warehouse":
                result = service.get_warehouse(data["id"])
                if not result:
                    response = {
                        "success": False,
                        "error": "Non trouve",
                    }
                else:
                    response["data"] = result.model_dump()

            elif action == "get_all_warehouses":
                results = service.get_all_warehouses()
                response["data"] = [
                    r.model_dump() for r in results
                ]

            elif action == "create_inventory":
                dto = CreateInventoryDTO(**data)
                result = service.create_inventory(dto)
                response["data"] = result.model_dump()

            elif action == "get":
                results = service.get_inventory_by_product(
                    data["product_pk"],
                )
                response["data"] = [
                    r.model_dump() for r in results
                ]

            elif action == "update":
                dto = UpdateInventoryDTO(
                    quantity=data["quantity"],
                )
                result = service.update_inventory(
                    data["warehouse_pk"],
                    data["product_pk"],
                    dto,
                )
                if not result:
                    response = {
                        "success": False,
                        "error": "Non trouve",
                    }
                else:
                    response["data"] = result.model_dump()

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
        if action == "get_nb_in_inventory":
            with Session(engine) as session:
                items = session.query(InventoryModel).filter_by(
                    product_pk=product_pk,
                ).all()
                total = sum(i.quantity for i in items)
                pair_socket.send_json({"quantity": total})
        else:
            pair_socket.send_json({"error": "unknown"})


def sub_events(ctx):
    """SUB thread: listen for product.created and orderline.created."""
    sub_product = ctx.socket(zmq.SUB)
    sub_product.connect("tcp://product-service:5560")
    sub_product.subscribe(b"product.created")

    sub_order = ctx.socket(zmq.SUB)
    sub_order.connect("tcp://order-service:5562")
    sub_order.subscribe(b"orderline.created")

    poller = zmq.Poller()
    poller.register(sub_product, zmq.POLLIN)
    poller.register(sub_order, zmq.POLLIN)

    while True:
        socks = dict(poller.poll())
        if sub_product in socks:
            msg = sub_product.recv_string()
            topic, payload = msg.split(" ", 1)
            data = json.loads(payload)
            on_product_created(data)
        if sub_order in socks:
            msg = sub_order.recv_string()
            topic, payload = msg.split(" ", 1)
            data = json.loads(payload)
            on_orderline_created(data)


def main():
    print("[inventory-service] Demarrage...")
    ctx = zmq.Context()

    rep = ctx.socket(zmq.REP)
    rep.bind("tcp://0.0.0.0:5557")

    pair = ctx.socket(zmq.PAIR)
    pair.bind("tcp://0.0.0.0:5564")

    threading.Thread(
        target=handle_pair, args=(pair,), daemon=True,
    ).start()
    threading.Thread(
        target=sub_events, args=(ctx,), daemon=True,
    ).start()

    print("[inventory-service] REP:5557 PAIR:5564 ready")

    while True:
        message = rep.recv_json()
        response = handle_request(message)
        rep.send_json(response)


if __name__ == "__main__":
    main()
