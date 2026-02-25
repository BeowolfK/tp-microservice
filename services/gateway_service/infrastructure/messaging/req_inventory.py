import zmq


class InventoryClient:
    def __init__(self, address: str = "tcp://inventory-service:5557"):
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

    def create_warehouse(self, data: dict) -> dict:
        return self._call("create_warehouse", data)

    def get_warehouse(self, warehouse_id: str) -> dict:
        return self._call("get_warehouse", {"id": warehouse_id})

    def get_all_warehouses(self) -> dict:
        return self._call("get_all_warehouses")

    def create_inventory(self, data: dict) -> dict:
        return self._call("create_inventory", data)

    def get_by_product(self, product_pk: str) -> dict:
        return self._call("get", {"product_pk": product_pk})

    def update(self, warehouse_pk: str, product_pk: str, quantity: int) -> dict:
        return self._call("update", {
            "warehouse_pk": warehouse_pk,
            "product_pk": product_pk,
            "quantity": quantity,
        })
