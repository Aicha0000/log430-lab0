from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from enum import Enum
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response
import time

app = FastAPI(title="Checkout Service", version="1.0.0")

REQUEST_COUNT = Counter('http_requests_total', 'Total requests', ['method', 'endpoint'])
REQUEST_DURATION = Histogram('http_request_duration_seconds', 'Request duration')

class PaymentMethod(str, Enum):
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    CASH = "cash"

class CheckoutRequest(BaseModel):
    customer_id: int
    items: List[dict]
    payment_method: PaymentMethod
    total_amount: float
    shipping_address: Optional[str] = None

class CheckoutStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    FAILED = "failed"

checkouts_db = {}
checkout_counter = 1

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

@app.post("/checkout/validate")
async def validate_checkout(checkout_data: CheckoutRequest):
    global checkout_counter
    
    if not checkout_data.items:
        raise HTTPException(status_code=400, detail="Panier vide")
    
    if checkout_data.total_amount <= 0:
        raise HTTPException(status_code=400, detail="Montant invalide")
    
    checkout = {
        "id": checkout_counter,
        "customer_id": checkout_data.customer_id,
        "items": checkout_data.items,
        "payment_method": checkout_data.payment_method,
        "total_amount": checkout_data.total_amount,
        "shipping_address": checkout_data.shipping_address,
        "status": CheckoutStatus.PENDING,
        "created_at": datetime.now()
    }
    
    checkouts_db[checkout_counter] = checkout
    checkout_counter += 1
    
    return {"checkout": checkout}

@app.post("/checkout/{checkout_id}/confirm")
async def confirm_checkout(checkout_id: int):
    if checkout_id not in checkouts_db:
        raise HTTPException(status_code=404, detail="Checkout not found")
    
    checkout = checkouts_db[checkout_id]
    checkout["status"] = CheckoutStatus.CONFIRMED
    checkout["confirmed_at"] = datetime.now()
    
    return {"message": "Checkout confirme", "checkout": checkout}

@app.get("/checkout/{checkout_id}")
async def get_checkout(checkout_id: int):
    if checkout_id not in checkouts_db:
        raise HTTPException(status_code=404, detail="Checkout not found")
    
    return {"checkout": checkouts_db[checkout_id]}

@app.get("/checkout/customer/{customer_id}")
async def get_customer_checkouts(customer_id: int):
    customer_checkouts = [
        checkout for checkout in checkouts_db.values() 
        if checkout["customer_id"] == customer_id
    ]
    
    customer_checkouts.sort(key=lambda x: x["created_at"], reverse=True)
    
    return {"checkouts": customer_checkouts}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8008)