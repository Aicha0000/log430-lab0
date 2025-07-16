#!/bin/bash

echo "Configuration des routes Kong API Gateway..."

KONG_ADMIN_URL="http://localhost:8001"

# Fonction pour créer un service et sa route
setup_service_and_route() {
    SERVICE_NAME=$1
    SERVICE_URL=$2
    ROUTE_PATH=$3
    
    echo "Création du service: $SERVICE_NAME"
    RESPONSE=$(curl -s -X POST $KONG_ADMIN_URL/services/ \
        --data "name=$SERVICE_NAME" \
        --data "url=$SERVICE_URL" 2>/dev/null)
    
    if [ $? -eq 0 ]; then
        echo "Service $SERVICE_NAME créé avec succès"
    else
        echo "Erreur lors de la création du service $SERVICE_NAME"
        return 1
    fi
    
    echo "Création de la route pour: $SERVICE_NAME"
    ROUTE_RESPONSE=$(curl -s -X POST $KONG_ADMIN_URL/services/$SERVICE_NAME/routes \
        --data "paths[]=$ROUTE_PATH" 2>/dev/null)
    
    if [ $? -eq 0 ]; then
        echo "Route $ROUTE_PATH créée avec succès"
    else
        echo "Erreur lors de la création de la route $ROUTE_PATH"
        return 1
    fi
}

setup_service_and_route "products-service" "http://products-service:8001" "/api/products"
setup_service_and_route "inventory-service" "http://inventory-service:8002" "/api/inventory"
setup_service_and_route "reports-service" "http://reports-service:8003" "/api/reports"
setup_service_and_route "sales-service" "http://sales-service:8004" "/api/sales"
setup_service_and_route "customer-service" "http://customer-service:8005" "/api/customers"
setup_service_and_route "order-service" "http://order-service:8006" "/api/orders"
setup_service_and_route "cart-service" "http://cart-service:8007" "/api/cart"
setup_service_and_route "checkout-service" "http://checkout-service:8008" "/api/checkout"

echo ""
echo "Configuration Kong terminée!"
echo "Gateway disponible à: http://localhost:8000"
echo "API Admin à: http://localhost:8001"
echo ""
echo "Services configurés:"
echo "  - Products: http://localhost:8000/api/products"
echo "  - Inventory: http://localhost:8000/api/inventory"
echo "  - Reports: http://localhost:8000/api/reports"
echo "  - Sales: http://localhost:8000/api/sales"
echo "  - Customers: http://localhost:8000/api/customers"
echo "  - Orders: http://localhost:8000/api/orders"
echo "  - Cart: http://localhost:8000/api/cart"
echo "  - Checkout: http://localhost:8000/api/checkout"
