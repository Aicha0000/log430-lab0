#!/bin/bash

echo "Setting up load balancing for cart service..."

KONG_ADMIN_URL="http://localhost:8001"

echo "Creating upstream for cart service"
curl -i -X POST $KONG_ADMIN_URL/upstreams \
    --data "name=cart-upstream" \
    --data "algorithm=round-robin"

echo "Adding cart service instances to upstream"
curl -i -X POST $KONG_ADMIN_URL/upstreams/cart-upstream/targets \
    --data "target=cart-service:8007" \
    --data "weight=100"

curl -i -X POST $KONG_ADMIN_URL/upstreams/cart-upstream/targets \
    --data "target=cart-service-2:8007" \
    --data "weight=100"

curl -i -X POST $KONG_ADMIN_URL/upstreams/cart-upstream/targets \
    --data "target=cart-service-3:8007" \
    --data "weight=100"

echo "Updating cart service to use upstream"
curl -i -X PATCH $KONG_ADMIN_URL/services/cart-service \
    --data "url=http://cart-upstream"

echo "Load balancing setup complete!"