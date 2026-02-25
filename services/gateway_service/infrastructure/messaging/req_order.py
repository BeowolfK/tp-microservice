import zmq


class OrderClient:
    def __init__(self, address: str = "tcp://order-service:5559"):
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

    def get(self, order_id: str) -> dict:
        return self._call("get", {"id": order_id})

    def update(self, order_id: str, data: dict) -> dict:
        data["id"] = order_id
        return self._call("update", data)
