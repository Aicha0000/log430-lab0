import http from 'k6/http';
import { check } from 'k6';

export let options = {
  vus: 20,
  duration: '30s',
};

export default function () {
  const baseUrl = 'http://localhost:8000';
  
  const endpoints = [
    '/api/products/health',
    '/api/inventory/health',
    '/api/customers/health',
    '/api/orders/health',
    '/api/reports/health',
    '/api/sales/health',
    '/api/reviews/health',
    '/api/notifications/health'
  ];
  
  const endpoint = endpoints[Math.floor(Math.random() * endpoints.length)];
  const response = http.get(`${baseUrl}${endpoint}`);
  
  check(response, {
    'status is 200': (r) => r.status === 200,
    'response time < 100ms': (r) => r.timings.duration < 100,
  });
}