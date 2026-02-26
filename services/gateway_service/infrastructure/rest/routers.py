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
    """Register API routes for all gateway services.

    Registers endpoints for product, customer, warehouse, inventory,
    pricing, and order operations. Each route delegates to the
    appropriate service.

    Parameters:
        router (APIRouter): FastAPI router instance.
        product_service: Product service client.
        customer_service: Customer service client.
        inventory_service: Inventory service client.
        pricing_service: Pricing service client.
        order_service: Order service client.

    Returns:
        APIRouter: The configured router with all registered routes.
    """
    # ──────────────────────────────────────────────
    # PRODUCT
    # ──────────────────────────────────────────────

    @router.post("/product", status_code=201)
    def create_product(body: dict):
        """Create a new product.

        Parameters:
            body (dict): Product data.

        Returns:
            dict: Created product data.

        Raises:
            HTTPException: If creation fails.
        """
        resp = product_service.create(body)
        if not resp.get("success"):
            raise HTTPException(status_code=400, detail=resp.get("error"))
        return resp["data"]

    @router.get("/product/{pk}")
    def get_product(pk: str):
        """Retrieve a product by ID.

        Parameters:
            pk (str): Product identifier.

        Returns:
            dict: Product data.

        Raises:
            HTTPException: If product not found.
        """
        resp = product_service.get(pk)
        if not resp.get("success"):
            raise HTTPException(status_code=404, detail=resp.get("error"))
        return resp["data"]

    @router.put("/product/{pk}")
    def update_product(pk: str, body: dict):
        """Update an existing product.

        Parameters:
            pk (str): Product identifier.
            body (dict): Updated product data.

        Returns:
            dict: Updated product data.

        Raises:
            HTTPException: If product not found or update fails.
        """
        resp = product_service.update(pk, body)
        if not resp.get("success"):
            raise HTTPException(status_code=404, detail=resp.get("error"))
        return resp["data"]

    # ──────────────────────────────────────────────
    # CUSTOMER
    # ──────────────────────────────────────────────

    @router.post("/customer", status_code=201)
    def create_customer(body: dict):
        """Create a new customer.

        Parameters:
            body (dict): Customer data.

        Returns:
            dict: Created customer data.

        Raises:
            HTTPException: If creation fails.
        """
        resp = customer_service.create(body)
        if not resp.get("success"):
            raise HTTPException(status_code=400, detail=resp.get("error"))
        return resp["data"]

    @router.get("/customer/{pk}")
    def get_customer(pk: str):
        """Retrieve a customer by ID.

        Parameters:
            pk (str): Customer identifier.

        Returns:
            dict: Customer data.

        Raises:
            HTTPException: If customer not found.
        """
        resp = customer_service.get(pk)
        if not resp.get("success"):
            raise HTTPException(status_code=404, detail=resp.get("error"))
        return resp["data"]

    # ──────────────────────────────────────────────
    # WAREHOUSE
    # ──────────────────────────────────────────────

    @router.post("/warehouse", status_code=201)
    def create_warehouse(body: dict):
        """Create a new warehouse.

        Parameters:
            body (dict): Warehouse data.

        Returns:
            dict: Created warehouse data.

        Raises:
            HTTPException: If creation fails.
        """
        resp = inventory_service.create_warehouse(body)
        if not resp.get("success"):
            raise HTTPException(status_code=400, detail=resp.get("error"))
        return resp["data"]

    @router.get("/warehouse")
    def get_all_warehouses():
        """Retrieve all warehouses.

        Returns:
            dict: List of warehouse data.

        Raises:
            HTTPException: If retrieval fails.
        """
        resp = inventory_service.get_all_warehouses()
        if not resp.get("success"):
            raise HTTPException(status_code=400, detail=resp.get("error"))
        return resp["data"]

    # ──────────────────────────────────────────────
    # INVENTORY
    # ──────────────────────────────────────────────

    @router.post("/inventory", status_code=201)
    def create_inventory(body: dict):
        """Create a new inventory item.

        Parameters:
            body (dict): Inventory data.

        Returns:
            dict: Created inventory data.

        Raises:
            HTTPException: If creation fails.
        """
        resp = inventory_service.create_inventory(body)
        if not resp.get("success"):
            raise HTTPException(status_code=400, detail=resp.get("error"))
        return resp["data"]

    @router.get("/inventory/{product_pk}")
    def get_inventory(product_pk: str):
        """Retrieve inventory for a product.

        Parameters:
            product_pk (str): Product identifier.

        Returns:
            dict: Inventory data for the product.

        Raises:
            HTTPException: If product not found or retrieval fails.
        """
        resp = inventory_service.get_by_product(product_pk)
        if not resp.get("success"):
            raise HTTPException(status_code=404, detail=resp.get("error"))
        return resp["data"]

    @router.patch("/inventory/{warehouse_pk}/{product_pk}")
    def update_inventory(warehouse_pk: str, product_pk: str, body: dict):
        """Update inventory quantity.

        Parameters:
            warehouse_pk (str): Warehouse identifier.
            product_pk (str): Product identifier.
            body (dict): Update data containing quantity.

        Returns:
            dict: Updated inventory data.

        Raises:
            HTTPException: If inventory not found or update fails.
        """
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
        """Create new pricing.

        Parameters:
            body (dict): Pricing data.

        Returns:
            dict: Created pricing data.

        Raises:
            HTTPException: If creation fails.
        """
        resp = pricing_service.create(body)
        if not resp.get("success"):
            raise HTTPException(status_code=400, detail=resp.get("error"))
        return resp["data"]

    @router.get("/pricing/{product_pk}")
    def get_pricing(product_pk: str):
        """Retrieve pricing for a product.

        Parameters:
            product_pk (str): Product identifier.

        Returns:
            dict: Pricing data for the product.

        Raises:
            HTTPException: If product not found or retrieval fails.
        """
        resp = pricing_service.get(product_pk)
        if not resp.get("success"):
            raise HTTPException(status_code=404, detail=resp.get("error"))
        return resp["data"]

    # ──────────────────────────────────────────────
    # ORDER
    # ──────────────────────────────────────────────

    @router.post("/order", status_code=201)
    def create_order(body: dict):
        """Create a new order.

        Parameters:
            body (dict): Order data.

        Returns:
            dict: Created order data.

        Raises:
            HTTPException: If creation fails.
        """
        resp = order_service.create(body)
        if not resp.get("success"):
            raise HTTPException(status_code=400, detail=resp.get("error"))
        return resp["data"]

    @router.get("/order/{pk}")
    def get_order(pk: str):
        """Retrieve an order by ID.

        Parameters:
            pk (str): Order identifier.

        Returns:
            dict: Order data.

        Raises:
            HTTPException: If order not found.
        """
        resp = order_service.get(pk)
        if not resp.get("success"):
            raise HTTPException(status_code=404, detail=resp.get("error"))
        return resp["data"]

    @router.patch("/order/{pk}")
    def update_order(pk: str, body: dict):
        """Update an order.

        Parameters:
            pk (str): Order identifier.
            body (dict): Updated order data.

        Returns:
            dict: Updated order data.

        Raises:
            HTTPException: If order not found or update fails.
        """
        resp = order_service.update(pk, body)
        if not resp.get("success"):
            raise HTTPException(status_code=404, detail=resp.get("error"))
        return resp["data"]

    return router
