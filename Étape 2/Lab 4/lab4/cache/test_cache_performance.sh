#!/bin/bash

echo "Test de Performance avec Cache Redis"
echo "====================================="

echo "Starting services..."
docker-compose up -d
sleep 45

echo "Test 1: Performance SANS cache (baseline)"
echo "Arret Redis pour forcer pas de cache..."
docker-compose stop redis
sleep 10
k6 run --duration 1m --vus 30 stress-test-cache.js > results_sans_cache.txt 2>&1
echo "Results sans cache sauvees dans results_sans_cache.txt"
echo ""

echo "Test 2: Performance AVEC cache Redis"
echo "Redemarrage Redis..."
docker-compose start redis
sleep 15
k6 run --duration 1m --vus 30 stress-test-cache.js > results_avec_cache.txt 2>&1
echo "Results avec cache sauvees dans results_avec_cache.txt"
echo ""

echo "Test 3: Cache hit/miss verification"
echo "Test rapide pour verifier que le cache marche..."
for i in {1..5}; do
    time curl -s -H "Authorization: Bearer lab3-static-token" http://localhost/api/central > /dev/null
    echo "Request $i done"
done

echo ""
echo "Tests complete! Compare results_sans_cache.txt vs results_avec_cache.txt"