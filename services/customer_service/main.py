import json
import zmq
from sqlalchemy.orm import Session

from services.customer_service.infrastructure.db.schema import Base, engine
from services.customer_service.application.dtos import (
    CreateCustomerDTO, UpdateCustomerDTO,
)
from services.customer_service.application.services.crud_service import (
    CustomerService,
)
from services.customer_service.domain.events import CUSTOMER_CREATED

Base.metadata.create_all(engine)

pub_socket = None


def handle_request(message: dict) -> dict:
    action = message.get("action")
    data = message.get("data", {})

    with Session(engine) as session:
        service = CustomerService(session)
        response = {"success": True, "data": None}

        try:
            if action == "create":
                dto = CreateCustomerDTO(**data)
                result = service.create(dto)
                response["data"] = result.model_dump()
                if pub_socket:
                    payload = json.dumps(response["data"])
                    pub_socket.send_string(
                        f"{CUSTOMER_CREATED} {payload}"
                    )

            elif action == "get":
                result = service.get(data["id"])
                if result is None:
                    response = {
                        "success": False,
                        "error": "Client non trouve",
                    }
                else:
                    response["data"] = result.model_dump()

            elif action == "get_all":
                results = service.get_all()
                response["data"] = [
                    r.model_dump() for r in results
                ]

            elif action == "update":
                customer_id = data.pop("id")
                dto = UpdateCustomerDTO(**data)
                result = service.update(customer_id, dto)
                if result is None:
                    response = {
                        "success": False,
                        "error": "Client non trouve",
                    }
                else:
                    response["data"] = result.model_dump()

            elif action == "delete":
                deleted = service.delete(data["id"])
                if not deleted:
                    response = {
                        "success": False,
                        "error": "Client non trouve",
                    }

            else:
                response = {
                    "success": False,
                    "error": f"Action inconnue: {action}",
                }

        except Exception as e:
            response = {"success": False, "error": str(e)}

    return response


def main():
    global pub_socket
    print("[customer-service] Demarrage...")
    ctx = zmq.Context()

    rep = ctx.socket(zmq.REP)
    rep.bind("tcp://0.0.0.0:5556")

    pub_socket = ctx.socket(zmq.PUB)
    pub_socket.bind("tcp://0.0.0.0:5561")

    print("[customer-service] REP:5556 PUB:5561 ready")

    while True:
        message = rep.recv_json()
        response = handle_request(message)
        rep.send_json(response)


if __name__ == "__main__":
    main()
