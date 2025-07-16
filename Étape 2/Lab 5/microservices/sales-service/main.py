from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response
import time

app = FastAPI(title="Sales Service", version="1.0.0")

REQUEST_COUNT = Counter('http_requests_total', 'Total requests', ['method', 'endpoint'])
REQUEST_DURATION = Histogram('http_request_duration_seconds', 'Request duration')

class VenteRequest(BaseModel):
    product_id: str
    magasin_id: str
    quantity: int
    prix_unitaire: float
    caissier_id: str = None

class SalesService:
    def __init__(self):
        self.ventes = []
        self.vente_counter = 1
    
    def create_vente(self, vente_data: VenteRequest):
        vente = {
            "id": self.vente_counter,
            "product_id": vente_data.product_id,
            "magasin_id": vente_data.magasin_id,
            "quantity": vente_data.quantity,
            "prix_unitaire": vente_data.prix_unitaire,
            "total": vente_data.quantity * vente_data.prix_unitaire,
            "caissier_id": vente_data.caissier_id,
            "date": datetime.now()
        }
        self.ventes.append(vente)
        self.vente_counter += 1
        return vente
    
    def get_ventes_par_magasin(self, magasin_id: str):
        return [vente for vente in self.ventes if vente["magasin_id"] == magasin_id]
    
    def get_ventes_today(self):
        today = datetime.now().date()
        return [vente for vente in self.ventes if vente["date"].date() == today]

sales_service = SalesService()

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

@app.post("/ventes")
async def create_vente(vente: VenteRequest):
    nouvelle_vente = sales_service.create_vente(vente)
    return {"vente": nouvelle_vente}

@app.get("/ventes/magasin/{magasin_id}")
async def get_ventes_magasin(magasin_id: str):
    ventes = sales_service.get_ventes_par_magasin(magasin_id)
    return {"ventes": ventes}

@app.get("/ventes/today")
async def get_ventes_today():
    ventes = sales_service.get_ventes_today()
    return {"ventes": ventes}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8004)