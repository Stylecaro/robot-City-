"""
🛒 Robot Comerciante — Puerto 8004
Tienda online automatizada con gestión de productos y pedidos.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timezone
import uvicorn
import uuid
import os

app = FastAPI(
    title="Robot Comerciante 🛒",
    description="Tienda online automatizada para Ciudad Robot",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

web_dir = os.path.join(os.path.dirname(__file__), "web")
if os.path.isdir(web_dir):
    app.mount("/web", StaticFiles(directory=web_dir), name="web")


# ── Models ──────────────────────────────────────────────────────────────────

class OrderRequest(BaseModel):
    customer_name: str
    product_id: str
    quantity: int = 1
    delivery_address: str
    contact_phone: Optional[str] = None


# ── In-memory storage ────────────────────────────────────────────────────────

orders: dict[str, dict] = {}

product_catalog = [
    {"id": "P001", "name": "Kit Robótico Básico", "price": 149.99, "stock": 15, "category": "robots"},
    {"id": "P002", "name": "Sensor Ultrasónico HC-SR04", "price": 4.99, "stock": 100, "category": "sensores"},
    {"id": "P003", "name": "Raspberry Pi 4 Model B", "price": 75.00, "stock": 20, "category": "computacion"},
    {"id": "P004", "name": "Arduino UNO Rev3", "price": 25.00, "stock": 50, "category": "microcontroladores"},
    {"id": "P005", "name": "Motor Servo SG90", "price": 3.50, "stock": 200, "category": "motores"},
    {"id": "P006", "name": "Batería LiPo 3000mAh", "price": 18.00, "stock": 40, "category": "energia"},
    {"id": "P007", "name": "Módulo WiFi ESP8266", "price": 6.00, "stock": 80, "category": "conectividad"},
    {"id": "P008", "name": "Cámara Pi NoIR", "price": 35.00, "stock": 25, "category": "vision"},
]


# ── Routes ───────────────────────────────────────────────────────────────────

@app.get("/health")
def health():
    return {
        "status": "online",
        "robot": "Robot Comerciante",
        "port": 8004,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/")
def root():
    return FileResponse(os.path.join(web_dir, "commerce.html"))


@app.get("/api/commerce/products")
def list_products(category: Optional[str] = None):
    products = product_catalog
    if category:
        products = [p for p in product_catalog if p["category"] == category]
    return {
        "products": products,
        "total": len(products),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.post("/api/commerce/order")
def place_order(req: OrderRequest):
    product = next((p for p in product_catalog if p["id"] == req.product_id), None)
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    if product["stock"] < req.quantity:
        raise HTTPException(status_code=400, detail="Stock insuficiente")

    product["stock"] -= req.quantity
    order_id = str(uuid.uuid4())
    order = {
        "id": order_id,
        "customer_name": req.customer_name,
        "product": product["name"],
        "product_id": req.product_id,
        "quantity": req.quantity,
        "total_price": round(product["price"] * req.quantity, 2),
        "delivery_address": req.delivery_address,
        "contact_phone": req.contact_phone,
        "status": "procesando",
        "estimated_delivery": "2-3 días hábiles",
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    orders[order_id] = order
    return {
        "message": "✅ Pedido realizado con éxito.",
        "order": order,
    }


@app.get("/api/commerce/order/{id}")
def get_order(id: str):
    order = orders.get(id)
    if not order:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return {"order": order}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8004)
