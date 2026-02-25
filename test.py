"""
Tests d'integration pour l'architecture microservices.
Prerequis : docker compose up --build -d
Usage     : pytest test.py -v
"""

import time
import pytest
import httpx

BASE_URL = "http://localhost:8000"


# ── Fixtures ─────────────────────────────────────────────────


@pytest.fixture(scope="session")
def client():
    """HTTP client shared across all tests."""
    # Wait for gateway
    for _ in range(30):
        try:
            r = httpx.get(f"{BASE_URL}/docs", timeout=2)
            if r.status_code == 200:
                break
        except httpx.ConnectError:
            pass
        time.sleep(1)
    else:
        pytest.fail("Gateway not reachable")

    with httpx.Client(base_url=BASE_URL, timeout=15) as c:
        yield c


@pytest.fixture(scope="session")
def product(client):
    """Create a product, return its data."""
    r = client.post("/product", json={
        "name": "MacBook Pro 14",
        "description": "Laptop Apple M3, 16Go RAM",
        "category": "electronics",
    })
    assert r.status_code == 201
    return r.json()


@pytest.fixture(scope="session")
def product2(client):
    """Create a second product."""
    r = client.post("/product", json={
        "name": "Python Fluent",
        "description": "Livre sur Python avance",
        "category": "books",
    })
    assert r.status_code == 201
    return r.json()


@pytest.fixture(scope="session")
def customer(client):
    """Create a customer, return its data."""
    r = client.post("/customer", json={
        "first_name": "Jean",
        "last_name": "Dupont",
        "email": "jean.dupont@example.com",
    })
    assert r.status_code == 201
    return r.json()


@pytest.fixture(scope="session")
def warehouse(client):
    """Create a warehouse, return its data."""
    r = client.post("/warehouse", json={
        "name": "Entrepot Paris",
        "location": "Paris, France",
    })
    assert r.status_code == 201
    return r.json()


@pytest.fixture(scope="session")
def warehouse2(client):
    """Create a second warehouse."""
    r = client.post("/warehouse", json={
        "name": "Entrepot Lyon",
        "location": "Lyon, France",
    })
    assert r.status_code == 201
    return r.json()


@pytest.fixture(scope="session")
def inventory(client, product, warehouse):
    """Create an inventory entry, return its data."""
    r = client.post("/inventory", json={
        "product_pk": product["id"],
        "warehouse_pk": warehouse["id"],
        "quantity": 100,
    })
    assert r.status_code == 201
    return r.json()


# ── PRODUCT — CRUD ───────────────────────────────────────────


class TestProductCRUD:
    def test_create_returns_201(self, product):
        assert len(product["id"]) == 36

    def test_create_name(self, product):
        assert product["name"] == "MacBook Pro 14"

    def test_create_available_default(self, product):
        assert product["available"] is True

    def test_create_second_product(self, product2):
        assert product2["name"] == "Python Fluent"

    def test_get(self, client, product):
        r = client.get(f"/product/{product['id']}")
        assert r.status_code == 200
        assert r.json()["name"] == "MacBook Pro 14"

    def test_update(self, client, product):
        r = client.put(f"/product/{product['id']}", json={
            "name": "MacBook Pro 16",
            "available": False,
        })
        assert r.status_code == 200
        data = r.json()
        assert data["name"] == "MacBook Pro 16"
        assert data["available"] is False


class TestProductErrors:
    def test_get_not_found(self, client):
        r = client.get("/product/id-inexistant")
        assert r.status_code == 404

    def test_update_not_found(self, client):
        r = client.put("/product/id-inexistant", json={"name": "Ghost"})
        assert r.status_code == 404

    def test_create_missing_category(self, client):
        r = client.post("/product", json={"name": "Sans categorie"})
        assert r.status_code == 400

    def test_create_blank_name(self, client):
        r = client.post("/product", json={
            "name": "   ",
            "category": "electronics",
        })
        assert r.status_code == 400

    def test_create_invalid_category(self, client):
        r = client.post("/product", json={
            "name": "Test",
            "category": "invalid_category",
        })
        assert r.status_code == 400


# ── CUSTOMER — CRUD ──────────────────────────────────────────


class TestCustomerCRUD:
    def test_create_returns_201(self, customer):
        assert len(customer["id"]) == 36

    def test_create_first_name(self, customer):
        assert customer["first_name"] == "Jean"

    def test_create_email(self, customer):
        assert customer["email"] == "jean.dupont@example.com"

    def test_get(self, client, customer):
        r = client.get(f"/customer/{customer['id']}")
        assert r.status_code == 200
        assert r.json()["last_name"] == "Dupont"


class TestCustomerErrors:
    def test_get_not_found(self, client):
        r = client.get("/customer/id-inexistant")
        assert r.status_code == 404


# ── WAREHOUSE — CRUD ─────────────────────────────────────────


class TestWarehouseCRUD:
    def test_create_returns_201(self, warehouse):
        assert warehouse["name"] == "Entrepot Paris"

    def test_create_second(self, warehouse2):
        assert warehouse2["name"] == "Entrepot Lyon"

    def test_get_all(self, client, warehouse, warehouse2):
        r = client.get("/warehouse")
        assert r.status_code == 200
        assert len(r.json()) >= 2


# ── INVENTORY — CRUD ─────────────────────────────────────────


class TestInventoryCRUD:
    def test_create_returns_201(self, inventory):
        assert inventory["quantity"] == 100

    def test_get_by_product(self, client, product, inventory):
        r = client.get(f"/inventory/{product['id']}")
        assert r.status_code == 200
        assert len(r.json()) >= 1

    def test_update(self, client, product, warehouse, inventory):
        r = client.patch(
            f"/inventory/{warehouse['id']}/{product['id']}",
            json={"quantity": 75},
        )
        assert r.status_code == 200
        assert r.json()["quantity"] == 75


class TestInventoryErrors:
    def test_get_nonexistent_product(self, client):
        r = client.get("/inventory/id-inexistant")
        assert r.status_code == 200
        assert r.json() == []


# ── PRICING — Event-driven ───────────────────────────────────


class TestPricingAutoCreated:
    def test_auto_created_on_product_created(self, client, product):
        time.sleep(1)
        r = client.get(f"/pricing/{product['id']}")
        assert r.status_code == 200
        pricing = r.json()
        assert pricing["price"] == 0.0
        assert pricing["product_pk"] == product["id"]

    def test_auto_created_for_new_product(self, client):
        r = client.post("/product", json={
            "name": "Clavier mecanique",
            "category": "electronics",
        })
        pid = r.json()["id"]
        time.sleep(1)
        r = client.get(f"/pricing/{pid}")
        assert r.status_code == 200


class TestPricingErrors:
    def test_get_not_found(self, client):
        r = client.get("/pricing/id-inexistant")
        assert r.status_code == 404


# ── ORDER — CRUD ─────────────────────────────────────────────


class TestOrderCRUD:
    @pytest.fixture(scope="class")
    def order(self, client, customer, product):
        r = client.post("/order", json={
            "customer_pk": customer["id"],
            "lines": [{
                "product_pk": product["id"],
                "quantity": 2,
                "unit_price": 1299.99,
            }],
        })
        assert r.status_code == 201
        return r.json()

    def test_create_status_pending(self, order):
        assert order["status"] == "pending"

    def test_create_has_one_line(self, order):
        assert len(order["lines"]) == 1

    def test_create_line_quantity(self, order):
        assert order["lines"][0]["quantity"] == 2

    def test_create_line_unit_price(self, order):
        assert order["lines"][0]["unit_price"] == 1299.99

    def test_create_customer_pk(self, order, customer):
        assert order["customer_pk"] == customer["id"]

    def test_create_has_created_at(self, order):
        assert "created_at" in order

    def test_get(self, client, order):
        r = client.get(f"/order/{order['id']}")
        assert r.status_code == 200
        assert r.json()["id"] == order["id"]
        assert len(r.json()["lines"]) == 1

    def test_update_confirmed(self, client, order):
        r = client.patch(
            f"/order/{order['id']}",
            json={"status": "confirmed"},
        )
        assert r.status_code == 200
        assert r.json()["status"] == "confirmed"

    def test_update_shipped(self, client, order):
        r = client.patch(
            f"/order/{order['id']}",
            json={"status": "shipped"},
        )
        assert r.status_code == 200
        assert r.json()["status"] == "shipped"

    def test_update_delivered(self, client, order):
        r = client.patch(
            f"/order/{order['id']}",
            json={"status": "delivered"},
        )
        assert r.status_code == 200
        assert r.json()["status"] == "delivered"


class TestOrderErrors:
    def test_get_not_found(self, client):
        r = client.get("/order/id-inexistant")
        assert r.status_code == 404

    def test_update_not_found(self, client):
        r = client.patch(
            "/order/id-inexistant",
            json={"status": "confirmed"},
        )
        assert r.status_code == 404


# ── EVENT — orderline.created decremente le stock ────────────


class TestEventOrderlineDecrementsInventory:
    def test_stock_decremented(self, client):
        # Isolated data
        r = client.post("/product", json={
            "name": "Casque Audio Test",
            "category": "electronics",
        })
        pid = r.json()["id"]

        r = client.post("/customer", json={
            "first_name": "Test",
            "last_name": "Event",
            "email": "test.event@example.com",
        })
        cid = r.json()["id"]

        r = client.post("/warehouse", json={
            "name": "Entrepot Test Event",
            "location": "Test",
        })
        wid = r.json()["id"]

        r = client.post("/inventory", json={
            "product_pk": pid,
            "warehouse_pk": wid,
            "quantity": 50,
        })
        assert r.status_code == 201

        r = client.get(f"/inventory/{pid}")
        items = [i for i in r.json() if i["warehouse_pk"] == wid]
        qty_before = items[0]["quantity"]
        assert qty_before == 50

        # Create order (triggers orderline.created event)
        r = client.post("/order", json={
            "customer_pk": cid,
            "lines": [{
                "product_pk": pid,
                "quantity": 3,
                "unit_price": 99.99,
            }],
        })
        assert r.status_code == 201

        time.sleep(3)

        r = client.get(f"/inventory/{pid}")
        items = [i for i in r.json() if i["warehouse_pk"] == wid]
        qty_after = items[0]["quantity"]
        assert qty_after == qty_before - 3


# ── WORKFLOW COMPLET — Parcours e-commerce ────────────────────


class TestFullWorkflow:
    def test_e_commerce_workflow(self, client):
        # 1. Create product
        r = client.post("/product", json={
            "name": "iPhone 16 Pro",
            "description": "Smartphone Apple",
            "category": "electronics",
        })
        assert r.status_code == 201
        product_id = r.json()["id"]

        # 2. Create customer
        r = client.post("/customer", json={
            "first_name": "Marie",
            "last_name": "Martin",
            "email": "marie.martin@example.com",
        })
        assert r.status_code == 201
        customer_id = r.json()["id"]

        # 3. Create warehouse
        r = client.post("/warehouse", json={
            "name": "Entrepot Nantes",
            "location": "Nantes, France",
        })
        assert r.status_code == 201
        warehouse_id = r.json()["id"]

        # 4. Pricing auto-created via event
        time.sleep(1)
        r = client.get(f"/pricing/{product_id}")
        assert r.status_code == 200

        # 5. Add stock
        r = client.post("/inventory", json={
            "product_pk": product_id,
            "warehouse_pk": warehouse_id,
            "quantity": 200,
        })
        assert r.status_code == 201

        # 6. Place order
        r = client.post("/order", json={
            "customer_pk": customer_id,
            "lines": [{
                "product_pk": product_id,
                "quantity": 5,
                "unit_price": 1199.99,
            }],
        })
        assert r.status_code == 201
        order_id = r.json()["id"]
        assert r.json()["status"] == "pending"

        # 7. Confirm
        r = client.patch(
            f"/order/{order_id}", json={"status": "confirmed"},
        )
        assert r.status_code == 200

        # 8. Ship
        r = client.patch(
            f"/order/{order_id}", json={"status": "shipped"},
        )
        assert r.status_code == 200

        # 9. Deliver
        r = client.patch(
            f"/order/{order_id}", json={"status": "delivered"},
        )
        assert r.status_code == 200
        assert r.json()["status"] == "delivered"
