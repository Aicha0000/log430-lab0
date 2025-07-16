from fastapi import FastAPI, HTTPException
from typing import Dict
from datetime import datetime, timedelta
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response
import time

app = FastAPI(title="Reports Service", version="1.0.0")

REQUEST_COUNT = Counter('http_requests_total', 'Total requests', ['method', 'endpoint'])
REQUEST_DURATION = Histogram('http_request_duration_seconds', 'Request duration')

class ReportsService:
    def __init__(self):
        self.sales_data = {
            "magasin_1": 15000,
            "magasin_2": 23000,
            "magasin_3": 18000
        }
        self.top_products = [
            {"id": "1", "name": "Coke", "ventes": 245},
            {"id": "2", "name": "Sprite", "ventes": 189},
            {"id": "3", "name": "Apple Juice", "ventes": 156},
            {"id": "4", "name": "Chocolate Milk", "ventes": 98},
            {"id": "5", "name": "Cafe", "ventes": 67}
        ]
    
    def generate_rapport(self, days: int = 30):
        return {
            "periode": f"{days} derniers jours",
            "ventes_par_magasin": self.sales_data,
            "top_produits": self.top_products,
            "total": sum(self.sales_data.values())
        }

reports_service = ReportsService()

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

@app.get("/reports/consolidated")
async def get_rapport_consolide(days: int = 30):
    rapport = reports_service.generate_rapport(days)
    return {"rapport": rapport}

@app.get("/reports/ventes")
async def get_rapport_ventes():
    return {"ventes_par_magasin": reports_service.sales_data}

@app.get("/reports/top-produits")
async def get_top_produits(limit: int = 5):
    produits = reports_service.top_products[:limit]
    return {"top_produits": produits}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)