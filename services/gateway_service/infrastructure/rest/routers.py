from fastapi import APIRouter, HTTPException

router = APIRouter()


def register_routes(
    router: APIRouter,
    product_service,
    customer_service,
    inventory_service,
    pricing_service,
    order_service,
):
    # ──────────────────────────────────────────────
    # PRODUCT
    # ──────────────────────────────────────────────

    @router.post("/product", status_code=201)
    def create_product(body: dict):
        resp = product_service.create(body)
        if not resp.get("success"):
            raise HTTPException(status_code=400, detail=resp.get("error"))
        return resp["data"]

    @router.get("/product/{pk}")
    def get_product(pk: str):
        resp = product_service.get(pk)
        if not resp.get("success"):
            raise HTTPException(status_code=404, detail=resp.get("error"))
        return resp["data"]

    @router.put("/product/{pk}")
    def update_product(pk: str, body: dict):
        resp = product_service.update(pk, body)
        if not resp.get("success"):
            raise HTTPException(status_code=404, detail=resp.get("error"))
        return resp["data"]

    # ──────────────────────────────────────────────
    # CUSTOMER
    # ──────────────────────────────────────────────

    @router.post("/customer", status_code=201)
    def create_customer(body: dict):
        resp = customer_service.create(body)
        if not resp.get("success"):
            raise HTTPException(status_code=400, detail=resp.get("error"))
        return resp["data"]

    @router.get("/customer/{pk}")
    def get_customer(pk: str):
        resp = customer_service.get(pk)
        if not resp.get("success"):
            raise HTTPException(status_code=404, detail=resp.get("error"))
        return resp["data"]

    # ──────────────────────────────────────────────
    # WAREHOUSE
    # ──────────────────────────────────────────────

    @router.post("/warehouse", status_code=201)
    def create_warehouse(body: dict):
        resp = inventory_service.create_warehouse(body)
        if not resp.get("success"):
            raise HTTPException(status_code=400, detail=resp.get("error"))
        return resp["data"]

    @router.get("/warehouse")
    def get_all_warehouses():
        resp = inventory_service.get_all_warehouses()
        if not resp.get("success"):
            raise HTTPException(status_code=400, detail=resp.get("error"))
        return resp["data"]

    # ──────────────────────────────────────────────
    # INVENTORY
    # ──────────────────────────────────────────────

    @router.post("/inventory", status_code=201)
    def create_inventory(body: dict):
        resp = inventory_service.create_inventory(body)
        if not resp.get("success"):
            raise HTTPException(status_code=400, detail=resp.get("error"))
        return resp["data"]

    @router.get("/inventory/{product_pk}")
    def get_inventory(product_pk: str):
        resp = inventory_service.get_by_product(product_pk)
        if not resp.get("success"):
            raise HTTPException(status_code=404, detail=resp.get("error"))
        return resp["data"]

    @router.patch("/inventory/{warehouse_pk}/{product_pk}")
    def update_inventory(warehouse_pk: str, product_pk: str, body: dict):
        quantity = body.get("quantity", 0)
        resp = inventory_service.update(warehouse_pk, product_pk, quantity)
        if not resp.get("success"):
            raise HTTPException(status_code=404, detail=resp.get("error"))
        return resp["data"]

    # ──────────────────────────────────────────────
    # PRICING
    # ──────────────────────────────────────────────

    @router.post("/pricing", status_code=201)
    def create_pricing(body: dict):
        resp = pricing_service.create(body)
        if not resp.get("success"):
            raise HTTPException(status_code=400, detail=resp.get("error"))
        return resp["data"]

    @router.get("/pricing/{product_pk}")
    def get_pricing(product_pk: str):
        resp = pricing_service.get(product_pk)
        if not resp.get("success"):
            raise HTTPException(status_code=404, detail=resp.get("error"))
        return resp["data"]

    # ──────────────────────────────────────────────
    # ORDER
    # ──────────────────────────────────────────────

    @router.post("/order", status_code=201)
    def create_order(body: dict):
        resp = order_service.create(body)
        if not resp.get("success"):
            raise HTTPException(status_code=400, detail=resp.get("error"))
        return resp["data"]

    @router.get("/order/{pk}")
    def get_order(pk: str):
        resp = order_service.get(pk)
        if not resp.get("success"):
            raise HTTPException(status_code=404, detail=resp.get("error"))
        return resp["data"]

    @router.patch("/order/{pk}")
    def update_order(pk: str, body: dict):
        resp = order_service.update(pk, body)
        if not resp.get("success"):
            raise HTTPException(status_code=404, detail=resp.get("error"))
        return resp["data"]

    return router
