import api from './api';

export interface ESewaPaymentParams {
  amt: number;
  psc: number;
  pdc: number;
  txAmt: number;
  tAmt: number;
  pid: string;
  scd: string;
  su: string;
  fu: string;
}

export interface ESewaInitiateResponse {
  payment_id: number;
  esewa_payload: Record<string, string>;  // all fields including esewa_url
  booking_id: string;
}

export const initiateESewaPayment = async (bookingId: string): Promise<ESewaInitiateResponse> => {
  const response = await api.post('/payments/esewa/initiate/', { booking_id: bookingId });
  return response.data;
};
export const verifyESewaPayment = async (data: string) => {
  const response = await api.get('/payments/esewa/verify/', {
    params: { data },  // v2 sends single 'data' param
  });
  return response.data;
};

// Submit form to eSewa
export const submitToESewa = (payload: Record<string, string>, url: string) => {
  const form = document.createElement('form');
  form.method = 'POST';
  form.action = url;

  Object.entries(payload).forEach(([key, value]) => {
    if (key === 'esewa_url') return; // skip — it's the action URL, not a field
    const input = document.createElement('input');
    input.type = 'hidden';
    input.name = key;
    input.value = String(value);
    form.appendChild(input);
  });

  document.body.appendChild(form);
  form.submit();
};

//   Object.entries(params).forEach(([key, value]) => {
//     const input = document.createElement('input');
//     input.type = 'hidden';
//     input.name = key;
//     input.value = String(value);
//     form.appendChild(input);
//   });

//   document.body.appendChild(form);
//   form.submit();
// };