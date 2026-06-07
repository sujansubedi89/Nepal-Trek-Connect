// ============================================================
// FILE: frontend/src/lib/payment.ts
// PURPOSE: eSewa epay v2 helpers.
//   - submitToESewa: creates hidden form and auto-submits to eSewa
//   - verifyESewaPayment: reads Base64 callback from eSewa
//
// NOTE: initiateESewaPayment removed — the booking creation endpoint
//   (POST /api/bookings/) now returns the esewa_payload directly.
// ============================================================

import api from './api';

// ── STEP 1 ──────────────────────────────────────────────────
// Dynamically create a hidden HTML form and POST it to eSewa.
// `payload`  — all the signed fields returned by Django in booking response
// `url`      — esewa_payload.esewa_url  (the eSewa sandbox/production endpoint)
export const submitToESewa = (
  payload: Record<string, string>,
  url: string
): void => {
  const form = document.createElement('form');
  form.method = 'POST';
  form.action = url;

  Object.entries(payload).forEach(([key, value]) => {
    if (key === 'esewa_url') return; // action URL, not a field

    const input = document.createElement('input');
    input.type = 'hidden';
    input.name = key;
    input.value = String(value);
    form.appendChild(input);
  });

  document.body.appendChild(form);
  form.submit();
};

// ── STEP 2 ──────────────────────────────────────────────────
// Called after eSewa redirects back to your success_url.
export const verifyESewaPayment = async (data: string) => {
  const response = await api.get('/bookings/esewa-verify/', {
    params: { data },
  });
  return response.data;
};