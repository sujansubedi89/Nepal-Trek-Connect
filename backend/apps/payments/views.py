import base64
import json
import uuid
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.conf import settings
from django.shortcuts import redirect
from .models import Payment
from .utils import generate_esewa_signature
from apps.bookings.models import Booking


class InitiateESewaPaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        booking_id = request.data.get('booking_id')

        try:
            booking = Booking.objects.get(booking_id=booking_id, user=request.user)
        except Booking.DoesNotExist:
            return Response({'error': 'Booking not found'}, status=404)

        conf = settings.ESEWA_SETTINGS

        # CRITICAL: Generate a NEW unique transaction_uuid every single attempt
        # eSewa sandbox rejects duplicate UUIDs with 409 Conflict
        transaction_uuid = f"{booking.booking_id}-{uuid.uuid4().hex[:8].upper()}"

        # Clean up old pending payments
        Payment.objects.filter(
            booking=booking,
            payment_method='esewa',
            status='pending'
        ).delete()

        # Create new payment record — store transaction_uuid as transaction_id
        payment = Payment.objects.create(
            transaction_id=transaction_uuid,
            booking=booking,
            user=request.user,
            payment_method='esewa',
            amount=booking.total_price,
            currency='NPR',
            status='pending'
        )

        # Amount MUST be formatted to exactly 2 decimal places
        # "854.05" in signature must exactly match "854.05" in form field
        amount_str = "{:.2f}".format(float(booking.total_price))

        signature = generate_esewa_signature(
            total_amount=amount_str,
            transaction_uuid=transaction_uuid,
            product_code=conf["MERCHANT_ID"],
            secret_key=conf["SECRET_KEY"]
        )

        esewa_payload = {
            "amount": amount_str,
            "tax_amount": "0",
            "total_amount": amount_str,
            "transaction_uuid": transaction_uuid,
            "product_code": conf["MERCHANT_ID"],
            "product_service_charge": "0",
            "product_delivery_charge": "0",
            "success_url": conf["SUCCESS_URL"],
            "failure_url": conf["FAILURE_URL"],
            "signed_field_names": "total_amount,transaction_uuid,product_code",
            "signature": signature,
            "esewa_url": conf["INITIATE_URL"],
        }

        # Debug log
        print(f"[eSewa] transaction_uuid: {transaction_uuid}")
        print(f"[eSewa] amount: {amount_str}")
        print(f"[eSewa] signature message: total_amount={amount_str},transaction_uuid={transaction_uuid},product_code={conf['MERCHANT_ID']}")
        print(f"[eSewa] signature: {signature}")

        return Response({
            'payment_id': payment.id,
            'esewa_payload': esewa_payload,
            'booking_id': booking.booking_id,
        })


class VerifyESewaPaymentView(APIView):
    # AllowAny because eSewa hits this URL directly (not the logged-in user)
    permission_classes = [AllowAny]

    def get(self, request):
        encoded_data = request.query_params.get('data')

        if not encoded_data:
            return redirect('http://localhost:3000/payment/failure?error=no_data')

        try:
            decoded_bytes = base64.b64decode(encoded_data)
            decoded_data = json.loads(decoded_bytes.decode('utf-8'))
            print(f"[eSewa Verify] decoded: {decoded_data}")
        except Exception as e:
            return redirect(f'http://localhost:3000/payment/failure?error=decode_failed')

        status_received = decoded_data.get('status')
        transaction_uuid = decoded_data.get('transaction_uuid')  # e.g. NTC19D00D64-AB12CD34
        esewa_ref = decoded_data.get('transaction_code')

        if status_received != 'COMPLETE':
            return redirect(f'http://localhost:3000/payment/failure?error=not_complete')

        try:
            payment = Payment.objects.get(transaction_id=transaction_uuid)
            booking = payment.booking
        except Payment.DoesNotExist:
            return redirect(f'http://localhost:3000/payment/failure?error=payment_not_found')

        # Update payment
        payment.status = 'completed'
        payment.gateway_response = decoded_data
        if esewa_ref:
            payment.transaction_id = esewa_ref
        payment.save()

        # Update booking
        booking.status = 'confirmed'
        booking.save()

        booking.trek.total_bookings += 1
        booking.trek.save()

        # Redirect to Next.js success page
        return redirect(
            f'http://localhost:3000/payment/success?booking_id={booking.booking_id}'
        )