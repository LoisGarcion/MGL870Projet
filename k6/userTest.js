import http from 'k6/http';
import { sleep } from 'k6';

export const options = {
  stages: [
    { duration: '5s', target: 2 }, // simulate ramp-up of traffic from 1 to 100 users over 30 seconds.
    { duration: '10s', target: 5 }, // stay at 100 users for 1 minutes
    { duration: '5s', target: 0 }, // ramp-down to 0 users
  ]
};

const BASE_URL1 = 'http://user-app:8080/api';
const BASE_URL2 = 'http://product-app:8080/api';
let cpt = 0;

export default function () {
    const createResponseuser = http.post(`${BASE_URL1}/user/create`, JSON.stringify({ name: `test-k6`, email: `test-k6@mail.com`, money: 500 }), {
      headers: { 'Content-Type': 'application/json' },
    });
    const createResponseproduct = http.post(`${BASE_URL2}/product/create`, JSON.stringify({ productName: `test-k62`, price: 200 }), {
        headers: { 'Content-Type': 'application/json' },
    });

    const createResponsebuy = http.post(`${BASE_URL1}/user/buy`, JSON.stringify({ productId: cpt, userId: cpt}), {
        headers: { 'Content-Type': 'application/json' },
    });

    // Perform read operation
    const readResponse = http.get(`${BASE_URL1}/user/all`);

    const readResponseId = http.get(`${BASE_URL1}/user/`+cpt);

    // Perform read operation
    const readResponse2 = http.get(`${BASE_URL2}/product/all`);
    const readResponseId2 = http.get(`${BASE_URL2}/product/`+cpt);
    cpt++;
    sleep(1);
}