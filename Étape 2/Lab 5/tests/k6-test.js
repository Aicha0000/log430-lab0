import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = {
  stages: [
    { duration: '30s', target: 20 },
    { duration: '1m', target: 50 },
    { duration: '30s', target: 0 },
  ],
};

const GATEWAY_URL = 'http://localhost:8000';
const DIRECT_URL = 'http://localhost:8008';

export default function() {
  let gateway_response = http.get(`${GATEWAY_URL}/api/cart/health`);
  check(gateway_response, {
    'gateway status is 200': (r) => r.status === 200,
    'gateway response time < 500ms': (r) => r.timings.duration < 500,
  });

  let direct_response = http.get(`${DIRECT_URL}/health`);
  check(direct_response, {
    'direct status is 200': (r) => r.status === 200,
    'direct response time < 500ms': (r) => r.timings.duration < 500,
  });

  sleep(1);
}