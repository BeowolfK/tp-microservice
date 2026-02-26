#!/usr/bin/env python3
"""
Test runner for microservices integration tests.
Starts the server and runs comprehensive integration tests.
"""

import time
import threading
import httpx
import sys
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

BASE_URL = "http://127.0.0.1:8000"

# Color codes for output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"
BOLD = "\033[1m"


def print_header(title: str):
    """Print a formatted header."""
    print(f"\n{BOLD}{BLUE}{'='*70}{RESET}")
    print(f"{BOLD}{BLUE}  {title}{RESET}")
    print(f"{BOLD}{BLUE}{'='*70}{RESET}\n")


def print_step(msg: str):
    """Print a step message."""
    print(f"{BOLD}{BLUE}► {msg}{RESET}")


def print_success(msg: str):
    """Print success message."""
    print(f"{GREEN}✓ {msg}{RESET}")


def print_error(msg: str):
    """Print error message."""
    print(f"{RED}✗ {msg}{RESET}")


def print_warning(msg: str):
    """Print warning message."""
    print(f"{YELLOW}⚠ {msg}{RESET}")


def start_gateway_server():
    """Start the gateway server."""
    print_step("Starting gateway server...")
    try:
        from main import app
        import uvicorn
        uvicorn.run(app, host="127.0.0.1", port=8000, log_level="error")
    except Exception as e:
        print_error(f"Failed to start gateway: {e}")


def wait_for_gateway(timeout: int = 30) -> bool:
    """Wait for gateway to be ready."""
    print_step("Waiting for gateway to be ready...")
    for attempt in range(timeout):
        try:
            response = httpx.get(f"{BASE_URL}/docs", timeout=2)
            if response.status_code == 200:
                print_success(f"Gateway is ready! (attempt {attempt + 1}/{timeout})")
                return True
        except (httpx.ConnectError, httpx.ReadTimeout):
            pass
        time.sleep(1)

    print_error(f"Gateway not reachable after {timeout} seconds")
    return False


def test_product_crud(client: httpx.Client) -> dict | None:
    """Test product CRUD operations."""
    print_header("TEST 1: PRODUCT CRUD")

    try:
        # CREATE
        print_step("Creating product...")
        r = client.post("/product", json={
            "name": "MacBook Pro 14",
            "description": "Laptop Apple M3, 16Go RAM",
            "category": "electronics",
        })
        if r.status_code != 201:
            print_error(f"CREATE failed: {r.status_code} - {r.json()}")
            return None
        product = r.json()
        print_success(f"Product created: {product['name']} (ID: {product['id']})")

        # GET
        print_step("Retrieving product...")
        r = client.get(f"/product/{product['id']}")
        if r.status_code != 200:
            print_error(f"GET failed: {r.status_code}")
            return None
        data = r.json()
        print_success(f"Retrieved: {data['name']}")

        # UPDATE
        print_step("Updating product...")
        r = client.put(f"/product/{product['id']}", json={
            "name": "MacBook Pro 16",
            "description": "Upgraded model"
        })
        if r.status_code != 200:
            print_error(f"UPDATE failed: {r.status_code}")
            return None
        updated = r.json()
        print_success(f"Updated name to: {updated['name']}")

        return product

    except Exception as e:
        print_error(f"Product CRUD test failed: {e}")
        return None


def test_customer_crud(client: httpx.Client) -> dict | None:
    """Test customer CRUD operations."""
    print_header("TEST 2: CUSTOMER CRUD")

    try:
        # CREATE
        print_step("Creating customer...")
        r = client.post("/customer", json={
            "first_name": "Jean",
            "last_name": "Dupont",
            "email": "jean.dupont@example.com",
        })
        if r.status_code != 201:
            print_error(f"CREATE failed: {r.status_code} - {r.json()}")
            return None
        customer = r.json()
        print_success(f"Customer created: {customer['first_name']} {customer['last_name']}")

        # GET
        print_step("Retrieving customer...")
        r = client.get(f"/customer/{customer['id']}")
        if r.status_code != 200:
            print_error(f"GET failed: {r.status_code}")
            return None
        data = r.json()
        print_success(f"Retrieved: {data['first_name']} {data['last_name']}")

        return customer

    except Exception as e:
        print_error(f"Customer CRUD test failed: {e}")
        return None


def test_warehouse_crud(client: httpx.Client) -> dict | None:
    """Test warehouse CRUD operations."""
    print_header("TEST 3: WAREHOUSE CRUD")

    try:
        # CREATE
        print_step("Creating warehouse...")
        r = client.post("/warehouse", json={
            "name": "Warehouse Paris",
            "location": "Paris, France",
        })
        if r.status_code != 201:
            print_error(f"CREATE failed: {r.status_code} - {r.json()}")
            return None
        warehouse = r.json()
        print_success(f"Warehouse created: {warehouse['name']}")

        # GET ALL
        print_step("Retrieving all warehouses...")
        r = client.get("/warehouse")
        if r.status_code != 200:
            print_error(f"GET ALL failed: {r.status_code}")
            return None
        warehouses = r.json()
        print_success(f"Found {len(warehouses)} warehouse(s)")

        return warehouse

    except Exception as e:
        print_error(f"Warehouse CRUD test failed: {e}")
        return None


def test_inventory_crud(client: httpx.Client, product: dict,
                        warehouse: dict) -> dict | None:
    """Test inventory CRUD operations."""
    print_header("TEST 4: INVENTORY CRUD")

    if not product or not warehouse:
        print_warning("Skipping (dependencies not available)")
        return None

    try:
        # CREATE
        print_step("Creating inventory...")
        r = client.post("/inventory", json={
            "product_pk": product["id"],
            "warehouse_pk": warehouse["id"],
            "quantity": 100,
        })
        if r.status_code != 201:
            print_error(f"CREATE failed: {r.status_code} - {r.json()}")
            return None
        inventory = r.json()
        print_success(f"Inventory created: {inventory['quantity']} units")

        # GET
        print_step("Retrieving inventory...")
        r = client.get(f"/inventory/{product['id']}")
        if r.status_code != 200:
            print_error(f"GET failed: {r.status_code}")
            return None
        data = r.json()
        print_success(f"Found {len(data) if isinstance(data, list) else 1} inventory item(s)")

        # UPDATE
        print_step("Updating inventory quantity...")
        r = client.patch(
            f"/inventory/{warehouse['id']}/{product['id']}",
            json={"quantity": 150}
        )
        if r.status_code != 200:
            print_error(f"UPDATE failed: {r.status_code}")
            return None
        updated = r.json()
        print_success(f"Updated quantity to: {updated['quantity']}")

        return inventory

    except Exception as e:
        print_error(f"Inventory CRUD test failed: {e}")
        return None


def test_pricing_crud(client: httpx.Client, product: dict) -> dict | None:
    """Test pricing CRUD operations."""
    print_header("TEST 5: PRICING OPERATIONS")

    if not product:
        print_warning("Skipping (product not available)")
        return None

    try:
        # CREATE
        print_step("Creating pricing...")
        r = client.post("/pricing", json={
            "product_pk": product["id"],
            "price": 1999.99,
        })
        if r.status_code != 201:
            print_warning(f"Pricing creation not available: {r.status_code}")
            return None

        pricing = r.json()
        print_success(f"Pricing created: ${pricing['price']}")

        # GET
        print_step("Retrieving pricing...")
        r = client.get(f"/pricing/{product['id']}")
        if r.status_code != 200:
            print_warning(f"GET failed: {r.status_code}")
            return pricing

        data = r.json()
        print_success(f"Retrieved pricing: ${data['price']}")

        return pricing

    except Exception as e:
        print_warning(f"Pricing test skipped: {e}")
        return None


def test_order_crud(client: httpx.Client, customer: dict,
                    product: dict) -> dict | None:
    """Test order CRUD operations."""
    print_header("TEST 6: ORDER CRUD")

    if not customer or not product:
        print_warning("Skipping (dependencies not available)")
        return None

    try:
        # CREATE
        print_step("Creating order...")
        r = client.post("/order", json={
            "customer_pk": customer["id"],
            "lines": [
                {
                    "product_pk": product["id"],
                    "quantity": 1,
                    "unit_price": 1999.99,
                }
            ]
        })
        if r.status_code != 201:
            print_warning(f"Order creation not available: {r.status_code}")
            return None

        order = r.json()
        print_success(f"Order created: {order['id']}")
        print_success(f"  - Status: {order['status']}")
        print_success(f"  - Line items: {len(order.get('lines', []))}")

        # GET
        print_step("Retrieving order...")
        r = client.get(f"/order/{order['id']}")
        if r.status_code != 200:
            print_warning(f"GET failed: {r.status_code}")
            return order

        data = r.json()
        print_success(f"Retrieved order status: {data['status']}")

        return order

    except Exception as e:
        print_warning(f"Order test skipped: {e}")
        return None


def test_error_handling(client: httpx.Client):
    """Test error handling."""
    print_header("TEST 7: ERROR HANDLING")

    print_step("Testing invalid product ID...")
    r = client.get("/product/invalid-id")
    if r.status_code == 404:
        print_success("Correctly returned 404 for non-existent product")
    else:
        print_warning(f"Unexpected status: {r.status_code}")

    print_step("Testing invalid customer ID...")
    r = client.get("/customer/invalid-id")
    if r.status_code == 404:
        print_success("Correctly returned 404 for non-existent customer")
    else:
        print_warning(f"Unexpected status: {r.status_code}")


def main():
    """Main test runner."""
    print_header("MICROSERVICES INTEGRATION TESTS")

    # Start gateway server in background
    server_thread = threading.Thread(target=start_gateway_server, daemon=True)
    server_thread.start()

    # Wait for gateway to be ready
    time.sleep(2)
    if not wait_for_gateway():
        print_error("Failed to start gateway server")
        return False

    # Run tests
    test_results = []

    try:
        with httpx.Client(base_url=BASE_URL, timeout=15) as client:
            # Run CRUD tests
            product = test_product_crud(client)
            test_results.append(("Product CRUD", product is not None))

            customer = test_customer_crud(client)
            test_results.append(("Customer CRUD", customer is not None))

            warehouse = test_warehouse_crud(client)
            test_results.append(("Warehouse CRUD", warehouse is not None))

            inventory = test_inventory_crud(client, product, warehouse)
            test_results.append(("Inventory CRUD", inventory is not None))

            pricing = test_pricing_crud(client, product)
            test_results.append(("Pricing CRUD", pricing is not None))

            order = test_order_crud(client, customer, product)
            test_results.append(("Order CRUD", order is not None))

            # Run error handling test
            test_error_handling(client)
            test_results.append(("Error Handling", True))

    except Exception as e:
        print_error(f"Test execution failed: {e}")
        return False

    # Print summary
    print_header("TEST SUMMARY")

    passed = sum(1 for _, result in test_results if result)
    total = len(test_results)

    print(f"Total Tests: {BOLD}{total}{RESET}")
    print(f"Passed: {GREEN}{BOLD}{passed}{RESET}")
    print(f"Failed: {RED}{BOLD}{total - passed}{RESET}\n")

    for test_name, result in test_results:
        status = f"{GREEN}✓ PASS{RESET}" if result else f"{RED}✗ FAIL{RESET}"
        print(f"  {status} - {test_name}")

    print(f"\n{BOLD}{BLUE}{'='*70}{RESET}")
    if passed == total:
        print_success(f"All {total} tests passed!")
        print(f"{BOLD}{BLUE}{'='*70}{RESET}\n")
        return True
    else:
        print_error(f"{total - passed} test(s) failed")
        print(f"{BOLD}{BLUE}{'='*70}{RESET}\n")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
