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
  esewa_params: ESewaPaymentParams;
  esewa_url: string;
  booking_id: string;
}

export const initiateESewaPayment = async (
  bookingId: string
): Promise<ESewaInitiateResponse> => {
  const response = await api.post('/payments/esewa/initiate/', {
    booking_id: bookingId,
  });
  return response.data;
};

export const verifyESewaPayment = async (
  oid: string,
  amt: string,
  refId: string
) => {
  const response = await api.get('/payments/esewa/verify/', {
    params: { oid, amt, refId },
  });
  return response.data;
};

// Submit form to eSewa
export const submitToESewa = (params: ESewaPaymentParams, url: string) => {
  const form = document.createElement('form');
  form.method = 'POST';
  form.action = url;

  Object.entries(params).forEach(([key, value]) => {
    const input = document.createElement('input');
    input.type = 'hidden';
    input.name = key;
    input.value = String(value);
    form.appendChild(input);
  });

  document.body.appendChild(form);
  form.submit();
};