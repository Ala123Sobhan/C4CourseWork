import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = {
  stages: [
    { duration: '5s', target: 10 },  // ramp-up from 0 to 10 virtual users in 1 minute - keeping it sec for test purposes
    { duration: '20s', target: 10 },  // stay at 10 virtual users for 5 minutes
    { duration: '5s', target: 0 },   // ramp-down to 0 users in 1 minute
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'], // 95% of requests should be under 500ms
    checks: ['rate>0.99'],
    http_req_failed: ['rate<0.01'],  
  },
};

export default function () {
  const url = 'https://api.stripe.com/v1/tokens';
  const payload = {
    email: 'ala+test_101@gmail.com',
    validation_type: 'card',
    payment_user_agent: 'Stripe Checkout v3 (stripe.js/78ef418)',
    'card[number]': '4242424242424242',
    'card[cvc]': '242',
    'card[exp_month]': '4',
    'card[exp_year]': '2028',
    'card[name]': 'a@gmail.com',
    'card[address_zip]': '10462',
    key: 'pk_test_TYooMQauvdEDq54NiTphI7jx',
  };

  const headers = {
    'accept': 'application/json',
    'accept-language': 'en-US',
    'content-type': 'application/x-www-form-urlencoded',
    'origin': 'https://checkout.stripe.com',
    'referer': 'https://checkout.stripe.com/',
  };

  const response = http.post(url, payload, { headers });

  // Check if the request was successful
  check(response, {
    'is status 200': (r) => r.status === 200,
    'contains expected token': (r) => r.body.includes('id'), // Ensure a response ID is returned, which indicates a valid token was created
  });

  // Parse the JSON response body
  const responseBody = JSON.parse(response.body);

  // Extract the token (if exists)
  const token = responseBody.id; // This assumes the token is in the 'id' field
  console.log('Extracted Token:', token); // Log the token to the console

 const Orderurl= 'https://weathershopper.pythonanywhere.com/confirmation';
 const orderPayload = {
    stripeToken: token,
    stripeTokenType: 'card',
    stripeEmail: 'ala+test_101@gmail.com',
  };
 const orderHeaders = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': 'https://weathershopper.pythonanywhere.com',
    'Referer': 'https://weathershopper.pythonanywhere.com/cart',
  };
  const orderResponse = http.post(Orderurl, orderPayload, { headers: orderHeaders });

  check(orderResponse, {
    'Order placed successfully': (r) => r.status === 200 && r.body.includes('Your payment was successful'),
  });

  sleep(1);  // Sleep between requests to simulate user think time


}
