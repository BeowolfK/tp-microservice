import zmq


class PricingClient:
    def __init__(self, address: str = "tcp://pricing-service:5558"):
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

    def get(self, product_pk: str) -> dict:
        return self._call("get", {"product_pk": product_pk})

    def update(self, product_pk: str, price: float) -> dict:
        return self._call("update", {
            "product_pk": product_pk,
            "price": price,
        })
