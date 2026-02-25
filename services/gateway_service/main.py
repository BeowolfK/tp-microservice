import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from services.gateway_service.infrastructure.messaging.req_product import ProductClient
from services.gateway_service.infrastructure.messaging.req_customer import CustomerClient
from services.gateway_service.infrastructure.messaging.req_inventory import InventoryClient
from services.gateway_service.infrastructure.messaging.req_pricing import PricingClient
from services.gateway_service.infrastructure.messaging.req_order import OrderClient

from services.gateway_service.application.services.product import ProductGatewayService
from services.gateway_service.application.services.customer import CustomerGatewayService
from services.gateway_service.application.services.inventory import InventoryGatewayService
from services.gateway_service.application.services.pricing import PricingGatewayService
from services.gateway_service.application.services.order import OrderGatewayService

from services.gateway_service.infrastructure.rest.routers import APIRouter, register_routes

app = FastAPI(title="Gateway API")


def setup():
    product_client = ProductClient()
    customer_client = CustomerClient()
    inventory_client = InventoryClient()
    pricing_client = PricingClient()
    order_client = OrderClient()

    product_svc = ProductGatewayService(product_client)
    customer_svc = CustomerGatewayService(customer_client)
    inventory_svc = InventoryGatewayService(inventory_client)
    pricing_svc = PricingGatewayService(pricing_client)
    order_svc = OrderGatewayService(order_client)

    router = APIRouter()
    register_routes(
        router, product_svc, customer_svc,
        inventory_svc, pricing_svc, order_svc,
    )
    app.include_router(router)


setup()

app.mount(
    "/static",
    StaticFiles(directory="services/gateway_service/static"),
    name="static",
)


@app.get("/")
def serve_frontend():
    return FileResponse("services/gateway_service/static/index.html")


def main():
    print("[gateway] Demarrage sur http://0.0.0.0:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
