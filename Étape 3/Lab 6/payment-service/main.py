from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import random
import time
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response

app = FastAPI(title="Payment Service", version="1.0.0")

class PaymentRequest(BaseModel):
    customer_id: int
    montant: float
    commande_id: str

class PaymentCancel(BaseModel):
    commande_id: str

# metriques
payment_requests = Counter('payment_requests_total', 'Total payment requests', ['resultat'])

# simulation stockage paiements
paiements_traites = {}

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "payment"}

@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.post("/payment/process")
async def process_payment(payment: PaymentRequest):
    print(f"Traitement paiement {payment.commande_id} - montant: {payment.montant}")
    
    # simulation delai traitement
    time.sleep(0.1)
    
    # simulation echec paiement (30% chance)
    if random.random() < 0.3:
        print(f"Paiement refuse pour {payment.commande_id}")
        payment_requests.labels(resultat="refuse").inc()
        raise HTTPException(status_code=400, detail="Paiement refuse")
    
    # paiement reussi
    paiement_data = {
        "commande_id": payment.commande_id,
        "customer_id": payment.customer_id,
        "montant": payment.montant,
        "status": "traite",
        "timestamp": time.time()
    }
    
    paiements_traites[payment.commande_id] = paiement_data
    payment_requests.labels(resultat="succes").inc()
    
    print(f"Paiement reussi pour {payment.commande_id}")
    
    return {
        "status": "success",
        "commande_id": payment.commande_id,
        "montant": payment.montant
    }

@app.post("/payment/cancel")
async def cancel_payment(cancel: PaymentCancel):
    print(f"Annulation paiement {cancel.commande_id}")
    
    if cancel.commande_id in paiements_traites:
        paiements_traites[cancel.commande_id]["status"] = "annule"
        return {"status": "cancelled", "commande_id": cancel.commande_id}
    
    return {"status": "not_found", "commande_id": cancel.commande_id}

@app.get("/payment/{commande_id}")
async def get_payment_status(commande_id: str):
    paiement = paiements_traites.get(commande_id)
    if not paiement:
        raise HTTPException(status_code=404, detail="Paiement non trouve")
    
    return paiement

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8009)