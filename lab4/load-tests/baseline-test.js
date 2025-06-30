import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = {
  stages: [
    { duration: '2m', target: 5 },
    { duration: '5m', target: 10 },
    { duration: '5m', target: 20 },
    { duration: '2m', target: 10 },
    { duration: '2m', target: 0 },
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'],
    http_req_failed: ['rate<0.05'],
  },
};

const API_URL = 'http://localhost:8000';
const TOKEN = 'lab3-static-token';

export default function () {
  let headers = {
    headers: {
      'Authorization': `Bearer ${TOKEN}`,
      'Content-Type': 'application/json',
    },
  };

  let random = Math.random();
  
  if (random < 0.6) {
    let resp = http.get(`${API_URL}/api/central`, headers);
    check(resp, {
      'stocks status 200': (r) => r.status === 200,
      'stocks response time < 500ms': (r) => r.timings.duration < 500,
    });
  } else if (random < 0.9) {
    let resp = http.get(`${API_URL}/api/consolide`, headers);
    check(resp, {
      'rapports status 200': (r) => r.status === 200,
      'rapports response time < 1000ms': (r) => r.timings.duration < 1000,
    });
  } else {
    let data = {
      name: `Produit Test ${Math.floor(Math.random() * 100)}`,
      price: Math.random() * 50 + 10,
      description: 'Test baseline'
    };
    
    let resp = http.put(`${API_URL}/api/produits/P001`, JSON.stringify(data), headers);
    check(resp, {
      'update status ok': (r) => r.status === 200 || r.status === 400,
    });
  }

  sleep(1);
}