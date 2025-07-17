from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import hashlib
from datetime import datetime
# import logging  # TODO: maybe add proper logging later
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response
import time

app = FastAPI(title="Customer Service", version="1.0.0")

# Metrics pour prometheus - copié du tuto
REQUEST_COUNT = Counter('http_requests_total', 'Total requests', ['method', 'endpoint'])
request_duration_hist = Histogram('http_request_duration_seconds', 'Request duration')

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

# Base de données temporaire - TODO: migrer vers vraie DB
client_database = {}
compteur_clients = 1
# customers_backup = {}  # pour debug si jamais

def hash_password(motdepasse: str) -> str:
    # Simple SHA256 hash - pas super secure mais bon
    return hashlib.sha256(motdepasse.encode()).hexdigest()
    # TODO: utiliser bcrypt ou quelque chose de mieux

@app.middleware("http")
async def metrics_middleware(request, call_next):
    debut = time.time()
    REQUEST_COUNT.labels(method=request.method, endpoint=request.url.path).inc()
    response = await call_next(request)
    temps_ecoule = time.time() - debut
    request_duration_hist.observe(temps_ecoule)
    # print(f"Request took {temps_ecoule}s")  # debug
    return response

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.post("/customers")
async def create_customer(donnees_client: CustomerCreate):
    global compteur_clients
    
    # Vérifier si email existe déjà
    for existing_client in client_database.values():
        if existing_client["email"] == donnees_client.email:
            print(f"Email {donnees_client.email} already exists!")  # debug
            raise HTTPException(status_code=400, detail="Email already exists")
    
    nouveau_client = {
        "id": compteur_clients,
        "email": donnees_client.email,
        "first_name": donnees_client.first_name,
        "last_name": donnees_client.last_name,
        "phone": donnees_client.phone,
        "address": donnees_client.address,
        "created_at": datetime.now()
    }
    
    client_database[compteur_clients] = nouveau_client
    compteur_clients += 1
    print(f"Nouveau client créé avec ID: {nouveau_client['id']}")  # debug
    
    return {"customer": nouveau_client}

@app.get("/customers/{customer_id}")
async def get_customer(customer_id: int):
    if customer_id not in client_database:
        print(f"Client {customer_id} pas trouvé")  # debug
        raise HTTPException(status_code=404, detail="Customer not found")
    
    client_info = client_database[customer_id]
    return {"customer": client_info}

@app.get("/customers/email/{email}")
async def get_customer_by_email(email: str):
    # Recherche par email - pas très efficace mais bon
    for client_id, client_data in client_database.items():
        if client_data["email"] == email:
            print(f"Client trouvé: {client_id}")  # debug
            return {"customer": client_data}
    
    print(f"Aucun client avec email: {email}")  # debug
    raise HTTPException(status_code=404, detail="Customer not found")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8005)
