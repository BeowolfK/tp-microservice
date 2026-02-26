import zmq


class CustomerClient:
    def __init__(self, address: str = "tcp://customer-service:5556"):
        self.address = address

    def _call(self, action: str, data: dict | None = None) -> dict:
        ctx = zmq.Context()
        sock = ctx.socket(zmq.REQ)
        sock.connect(self.address)
        try:
            sock.send_json({"action": action, "data": data or {}})
            return sock.recv_json()
        finally:
            sock.close()
            ctx.term()

    def create(self, data: dict) -> dict:
        return self._call("create", data)

    def get(self, customer_id: str) -> dict:
        return self._call("get", {"id": customer_id})

    def get_all(self) -> dict:
        return self._call("get_all")

    def update(self, customer_id: str, data: dict) -> dict:
        data["id"] = customer_id
        return self._call("update", data)

    def delete(self, customer_id: str) -> dict:
        return self._call("delete", {"id": customer_id})
