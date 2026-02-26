import time
import threading
import httpx
import uvicorn
from fastapi import FastAPI

from services.product_service.infrastructure.db.models import Base, engine
from services.product_service.infrastructure.rest.route import router

Base.metadata.create_all(engine)

app = FastAPI()
app.include_router(router)

BASE_URL = "http://127.0.0.1:8000"


def start_server():
    """Start the FastAPI server.

    Runs the uvicorn server with the configured FastAPI application
    on localhost port 8000.

    Returns:
        None
    """
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="error")


def check(label, response, expected_status):
    """Check and display HTTP response status.

    Compares the actual HTTP response status code against the expected
    value and prints the result with the response body if available.

    Parameters:
        label (str): Description of the test case.
        response: HTTP response object from httpx.
        expected_status (int): Expected HTTP status code.

    Returns:
        None
    """
    status = "✓" if response.status_code == expected_status else "✗"
    print(f"\n{status} {label}")
    print(f"  → status  : {response.status_code} (attendu {expected_status})")
    if response.content:
        print(f"  → réponse : {response.json()}")


if __name__ == "__main__":
    thread = threading.Thread(target=start_server, daemon=True)
    thread.start()
    time.sleep(1)

    with httpx.Client(base_url=BASE_URL) as client:
        print("=" * 55)
        print("TESTS CRUD — /products")
        print("=" * 55)

        # --- CAS NOMINAUX ---
        print("\n── Cas nominaux ──────────────────────────────────────")

        # CREATE #1
        r = client.post("/products/", json={
            "name": "MacBook Pro 14",
            "description": "Laptop Apple M3, 16Go RAM",
            "category": "electronics",
        })
        check("CREATE MacBook Pro 14", r, 201)
        product_id = r.json()["id"]

        # CREATE #2
        r = client.post("/products/", json={
            "name": "Python Fluent",
            "description": "Livre sur Python avancé",
            "category": "books",
        })
        check("CREATE Python Fluent", r, 201)
        book_id = r.json()["id"]

        # GET ALL (2 produits)
        r = client.get("/products/")
        check("GET ALL (2 produits attendus)", r, 200)
        print(f"  → nb produits : {len(r.json())}")

        # UPDATE partiel (nom + available)
        r = client.patch(f"/products/{product_id}", json={
            "name": "MacBook Pro 16",
            "available": False,
        })
        check("UPDATE nom + available", r, 200)

        # UPDATE catégorie uniquement
        r = client.patch(f"/products/{book_id}", json={
            "category": "other",
        })
        check("UPDATE catégorie uniquement", r, 200)

        # DELETE #1
        r = client.delete(f"/products/{product_id}")
        check("DELETE MacBook Pro 16", r, 204)

        # GET ALL (1 produit restant)
        r = client.get("/products/")
        check("GET ALL (1 produit attendu)", r, 200)
        print(f"  → nb produits : {len(r.json())}")

        # DELETE #2
        r = client.delete(f"/products/{book_id}")
        check("DELETE Python Fluent", r, 204)

        # GET ALL (vide)
        r = client.get("/products/")
        check("GET ALL (0 produit attendu)", r, 200)
        print(f"  → nb produits : {len(r.json())}")

        # --- CAS D'ERREUR ---
        print("\n── Cas d'erreur ──────────────────────────────────────")

        # UPDATE sur id inexistant
        r = client.patch("/products/id-inexistant", json={"name": "Ghost"})
        check("UPDATE id inexistant (404 attendu)", r, 404)

        # DELETE sur id inexistant
        r = client.delete("/products/id-inexistant")
        check("DELETE id inexistant (404 attendu)", r, 404)

        # CREATE sans champ obligatoire (category manquante)
        r = client.post("/products/", json={"name": "Produit sans catégorie"})
        check("CREATE sans category (422 attendu)", r, 422)

        # CREATE avec nom vide
        r = client.post("/products/", json={
            "name": "   ",
            "category": "electronics",
        })
        check("CREATE nom vide/espaces (422 attendu)", r, 422)

        # CREATE avec catégorie invalide
        r = client.post("/products/", json={
            "name": "Produit test",
            "category": "invalid_category",
        })
        check("CREATE catégorie invalide (422 attendu)", r, 422)

        print("\n" + "=" * 55)
