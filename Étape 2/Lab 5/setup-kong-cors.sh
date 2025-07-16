#!/bin/bash

echo "Configuring CORS for Kong Gateway..."

KONG_ADMIN_URL="http://localhost:8001"

echo "Adding CORS plugin globally"
curl -i -X POST $KONG_ADMIN_URL/plugins/ \
    --data "name=cors" \
    --data "config.origins=*" \
    --data "config.methods=GET,POST,PUT,DELETE,OPTIONS" \
    --data "config.headers=Accept,Accept-Version,Content-Length,Content-MD5,Content-Type,Date,X-Auth-Token,Authorization" \
    --data "config.exposed_headers=X-Auth-Token" \
    --data "config.credentials=true" \
    --data "config.max_age=3600"

echo "CORS configuration complete!"