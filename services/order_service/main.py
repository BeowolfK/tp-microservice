import json
import threading
import zmq
from sqlalchemy.orm import Session

from services.order_service.infrastructure.db.schema import Base, engine
from services.order_service.application.dtos import (
    CreateOrderDTO, UpdateOrderDTO,
)
from services.order_service.application.services.crud_service import (
    OrderService,
)
from services.order_service.domain.events import (
    ORDER_CREATED, ORDERLINE_CREATED,
)

Base.metadata.create_all(engine)

pub_socket = None


def handle_request(message: dict) -> dict:
    action = message.get("action")
    data = message.get("data", {})

    with Session(engine) as session:
        service = OrderService(session)
        response = {"success": True, "data": None}

        try:
            if action == "create":
                dto = CreateOrderDTO(**data)
                result = service.create(dto)
                response["data"] = result.model_dump()
                if pub_socket:
                    # Publish order.created
                    order_data = json.dumps({
                        "id": response["data"]["id"],
                        "customer_pk": response["data"]["customer_pk"],
                    })
                    pub_socket.send_string(
                        f"{ORDER_CREATED} {order_data}"
                    )
                    # Publish orderline.created for each line
                    for line in response["data"]["lines"]:
                        line_data = json.dumps(line)
                        pub_socket.send_string(
                            f"{ORDERLINE_CREATED} {line_data}"
                        )

            elif action == "get":
                result = service.get(data["id"])
                if result is None:
                    response = {
                        "success": False,
                        "error": "Non trouve",
                    }
                else:
                    response["data"] = result.model_dump()

            elif action == "update":
                order_id = data.pop("id")
                dto = UpdateOrderDTO(**data)
                result = service.update_status(order_id, dto)
                if result is None:
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


def sub_events(ctx):
    """SUB thread: listen for product.created and customer.created."""
    sub_product = ctx.socket(zmq.SUB)
    sub_product.connect("tcp://product-service:5560")
    sub_product.subscribe(b"product.created")

    sub_customer = ctx.socket(zmq.SUB)
    sub_customer.connect("tcp://customer-service:5561")
    sub_customer.subscribe(b"customer.created")

    poller = zmq.Poller()
    poller.register(sub_product, zmq.POLLIN)
    poller.register(sub_customer, zmq.POLLIN)

    while True:
        socks = dict(poller.poll())
        if sub_product in socks:
            msg = sub_product.recv_string()
            topic, payload = msg.split(" ", 1)
            data = json.loads(payload)
            print(f"[order-service] product.created: {data.get('id')}")
        if sub_customer in socks:
            msg = sub_customer.recv_string()
            topic, payload = msg.split(" ", 1)
            data = json.loads(payload)
            print(f"[order-service] customer.created: {data.get('id')}")


def main():
    global pub_socket
    print("[order-service] Demarrage...")
    ctx = zmq.Context()

    rep = ctx.socket(zmq.REP)
    rep.bind("tcp://0.0.0.0:5559")

    pub_socket = ctx.socket(zmq.PUB)
    pub_socket.bind("tcp://0.0.0.0:5562")

    threading.Thread(
        target=sub_events, args=(ctx,), daemon=True,
    ).start()

    print("[order-service] REP:5559 PUB:5562 ready")

    while True:
        message = rep.recv_json()
        response = handle_request(message)
        rep.send_json(response)


if __name__ == "__main__":
    main()
