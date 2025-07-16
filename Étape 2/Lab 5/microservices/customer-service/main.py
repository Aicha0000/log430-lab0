from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import hashlib
from datetime import datetime
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response
import time

app = FastAPI(title="Customer Service", version="1.0.0")

REQUEST_COUNT = Counter('http_requests_total', 'Total requests', ['method', 'endpoint'])
REQUEST_DURATION = Histogram('http_request_duration_seconds', 'Request duration')

class CustomerCreate(BaseModel):
    email: str
    first_name: str
    last_name: str
    password: str
    phone: Optional[str] = None
    address: Optional[str] = None

class Customer(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    phone: Optional[str] = None
    address: Optional[str] = None
    created_at: datetime
    loyalty_points: int = 0

customers_db = {}
customer_counter = 1

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

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

@app.post("/customers")
async def create_customer(customer_data: CustomerCreate):
    global customer_counter
    
    for customer in customers_db.values():
        if customer["email"] == customer_data.email:
            raise HTTPException(status_code=400, detail="Email already exists")
    
    customer = {
        "id": customer_counter,
        "email": customer_data.email,
        "first_name": customer_data.first_name,
        "last_name": customer_data.last_name,
        "phone": customer_data.phone,
        "address": customer_data.address,
        "created_at": datetime.now(),
        "loyalty_points": 100
    }
    
    customers_db[customer_counter] = customer
    customer_counter += 1
    
    return {"customer": customer}

@app.get("/customers/{customer_id}")
async def get_customer(customer_id: int):
    if customer_id not in customers_db:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    return {"customer": customers_db[customer_id]}

@app.get("/customers/email/{email}")
async def get_customer_by_email(email: str):
    for customer in customers_db.values():
        if customer["email"] == email:
            return {"customer": customer}
    
    raise HTTPException(status_code=404, detail="Customer not found")

@app.put("/customers/{customer_id}/loyalty")
async def update_loyalty_points(customer_id: int, points: int):
    if customer_id not in customers_db:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    customers_db[customer_id]["loyalty_points"] += points
    return {
        "message": "Loyalty points updated", 
        "total_points": customers_db[customer_id]["loyalty_points"]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8005)
