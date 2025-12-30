from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated ,AllowAny
from django.conf import settings
import requests
import hashlib
from .models import Payment
from apps.bookings.models import Booking

class InitiateESewaPaymentView(APIView):
    """Generate eSewa payment parameters"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        booking_id = request.data.get('booking_id')
        
        try:
            booking = Booking.objects.get(booking_id=booking_id, user=request.user)
        except Booking.DoesNotExist:
            return Response(
                {'error': 'Booking not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Create payment record
        payment = Payment.objects.create(
            transaction_id=f"ESEWA-{booking.booking_id}",
            booking=booking,
            user=request.user,
            payment_method='esewa',
            amount=booking.total_price,
            currency='NPR',
            status='pending'
        )
        
        # Calculate amount (eSewa works in Paisa, so multiply by 100)
        amount = float(booking.total_price)
        
        # eSewa payment parameters
        esewa_params = {
            'amt': amount,
            'psc': 0,  # Service charge
            'pdc': 0,  # Delivery charge
            'txAmt': 0,  # Tax amount
            'tAmt': amount,  # Total amount
            'pid': booking.booking_id,  # Product/Booking ID
            'scd': settings.ESEWA_MERCHANT_CODE,
            'su': settings.ESEWA_SUCCESS_URL,
            'fu': settings.ESEWA_FAILURE_URL,
        }
        
        return Response({
            'payment_id': payment.id,
            'esewa_params': esewa_params,
            'esewa_url': settings.ESEWA_PAYMENT_URL,
            'booking_id': booking.booking_id,
        })


class VerifyESewaPaymentView(APIView):
    """Verify eSewa payment after redirect"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # eSewa sends these parameters after payment
        oid = request.query_params.get('oid')  # Booking ID
        amt = request.query_params.get('amt')  # Amount
        refId = request.query_params.get('refId')  # eSewa reference ID
        
        if not all([oid, amt, refId]):
            return Response(
                {'error': 'Missing payment parameters'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            booking = Booking.objects.get(booking_id=oid, user=request.user)
        except Booking.DoesNotExist:
            return Response(
                {'error': 'Booking not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Verify payment with eSewa
        verify_url = settings.ESEWA_VERIFY_URL
        verify_params = {
            'amt': amt,
            'scd': settings.ESEWA_MERCHANT_CODE,
            'rid': refId,
            'pid': oid,
        }
        
        try:
            response = requests.get(verify_url, params=verify_params)
            
            # eSewa returns XML with "Success" or "Failure"
            if 'Success' in response.text:
                # Payment verified successfully
                payment = Payment.objects.filter(
                    booking=booking,
                    payment_method='esewa'
                ).first()
                
                if payment:
                    payment.transaction_id = refId
                    payment.status = 'completed'
                    payment.gateway_response = {
                        'response': response.text,
                        'refId': refId,
                        'amount': amt
                    }
                    payment.save()
                
                # Update booking status
                booking.status = 'confirmed'
                booking.save()
                
                # Update trek stats
                booking.trek.total_bookings += 1
                booking.trek.save()
                
                return Response({
                    'success': True,
                    'message': 'Payment verified successfully',
                    'booking_id': booking.booking_id,
                    'payment_id': payment.id if payment else None,
                    'reference_id': refId
                })
            else:
                return Response(
                    {'error': 'Payment verification failed', 'response': response.text},
                    status=status.HTTP_400_BAD_REQUEST
                )
                
        except Exception as e:
            return Response(
                {'error': f'Verification error: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )