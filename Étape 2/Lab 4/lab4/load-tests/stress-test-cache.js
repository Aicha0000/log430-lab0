import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = {
  stages: [
    { duration: '30s', target: 10 },
    { duration: '1m', target: 25 },
    { duration: '1m', target: 50 },
    { duration: '30s', target: 0 },
  ],
  thresholds: {
    http_req_duration: ['p(95)<2000'],
    http_req_failed: ['rate<0.1'],
  },
};

const API_URL = 'http://localhost';
const TOKEN = 'lab3-static-token';

export default function () {
  let headers = {
    headers: {
      'Authorization': `Bearer ${TOKEN}`,
      'Content-Type': 'application/json',
    },
  };

  let random = Math.random();
  
  if (random < 0.7) {
    let resp = http.get(`${API_URL}/api/central`, headers);
    check(resp, {
      'stocks ok': (r) => r.status === 200,
    });
  } else if (random < 0.95) {
    let resp = http.get(`${API_URL}/api/consolide`, headers);
    check(resp, {
      'rapports ok': (r) => r.status === 200,
    });
  } else {
    let data = {
      name: `Test Product ${Math.floor(Math.random() * 100)}`,
      price: Math.random() * 50 + 10,
      description: 'test cache invalidation'
    };
    
    let resp = http.put(`${API_URL}/api/produits/P001`, JSON.stringify(data), headers);
    check(resp, {
      'update ok': (r) => r.status === 200 || r.status === 400,
    });
  }

  sleep(0.3);
}