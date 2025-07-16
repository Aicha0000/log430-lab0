from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from enum import Enum
import requests
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response
import time

app = FastAPI(title="Order Service", version="1.0.0")

REQUEST_COUNT = Counter('http_requests_total', 'Total requests', ['method', 'endpoint'])
REQUEST_DURATION = Histogram('http_request_duration_seconds', 'Request duration')

class OrderStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PROCESSING = "processing"
    READY = "ready"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class OrderItem(BaseModel):
    product_id: str
    quantity: int
    unit_price: float

class OrderCreate(BaseModel):
    customer_id: int
    items: List[OrderItem]
    store_id: str
    delivery_address: Optional[str] = None

class Order(BaseModel):
    id: int
    customer_id: int
    items: List[OrderItem]
    store_id: str
    status: OrderStatus
    total_amount: float
    delivery_address: Optional[str] = None
    created_at: datetime
    updated_at: datetime

orders_db = {}
order_counter = 1

def validate_customer(customer_id: int) -> bool:
    try:
        response = requests.get(f"http://customer-service:8005/customers/{customer_id}", timeout=3)
        return response.status_code == 200
    except:
        return False

def validate_products(items: List[OrderItem]) -> bool:
    try:
        for item in items:
            response = requests.get(f"http://products-service:8001/products/{item.product_id}", timeout=3)
            if response.status_code != 200:
                return False
        return True
    except:
        return False

@app.middleware("http")
async def metrics_middleware(request, call_next):
    start_time = time.time()
    REQUEST_COUNT.labels(method=request.method, endpoint=request.url.path).inc()
    response = await call_next(request)
    REQUEST_DURATION.observe(time.time() - start_time)
    return response

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.post("/orders")
async def create_order(order_data: OrderCreate):
    global order_counter
    
    if not validate_customer(order_data.customer_id):
        raise HTTPException(status_code=400, detail="Invalid customer")
    
    if not validate_products(order_data.items):
        raise HTTPException(status_code=400, detail="Invalid products")
    
    total = sum(item.quantity * item.unit_price for item in order_data.items)
    
    order = {
        "id": order_counter,
        "customer_id": order_data.customer_id,
        "items": [item.dict() for item in order_data.items],
        "store_id": order_data.store_id,
        "status": OrderStatus.PENDING,
        "total_amount": total,
        "delivery_address": order_data.delivery_address,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }
    
    orders_db[order_counter] = order
    order_counter += 1
    
    try:
        requests.post(f"http://notification-service:8008/notifications/order-created", 
                     json={"order_id": order["id"], "customer_id": order["customer_id"]}, 
                     timeout=3)
    except:
        pass
    
    return {"order": order}

@app.get("/orders/{order_id}")
async def get_order(order_id: int):
    if order_id not in orders_db:
        raise HTTPException(status_code=404, detail="Order not found")
    
    return {"order": orders_db[order_id]}

@app.get("/orders/customer/{customer_id}")
async def get_customer_orders(customer_id: int):
    customer_orders = [order for order in orders_db.values() if order["customer_id"] == customer_id]
    return {"orders": customer_orders}

@app.put("/orders/{order_id}/status")
async def update_order_status(order_id: int, status: OrderStatus):
    if order_id not in orders_db:
        raise HTTPException(status_code=404, detail="Order not found")
    
    orders_db[order_id]["status"] = status
    orders_db[order_id]["updated_at"] = datetime.now()
    
    try:
        requests.post(f"http://notification-service:8008/notifications/order-updated", 
                     json={"order_id": order_id, "status": status}, 
                     timeout=3)
    except:
        pass
    
    return {"message": "Order status updated", "order": orders_db[order_id]}

@app.post("/orders/{order_id}/checkout")
async def checkout_order(order_id: int):
    if order_id not in orders_db:
        raise HTTPException(status_code=404, detail="Order not found")
    
    order = orders_db[order_id]
    if order["status"] != OrderStatus.PENDING:
        raise HTTPException(status_code=400, detail="Order cannot be checked out")
    
    orders_db[order_id]["status"] = OrderStatus.CONFIRMED
    orders_db[order_id]["updated_at"] = datetime.now()
    
    try:
        requests.post(f"http://notification-service:8008/notifications/order-confirmed", 
                     json={"order_id": order_id, "customer_id": order["customer_id"]}, 
                     timeout=3)
    except:
        pass
    
    return {"message": "Order confirmed", "order": orders_db[order_id]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8006)
