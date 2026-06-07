import base64
import json

from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Booking
from .payment_strategies import EsewaStrategy
from .serializers import BookingCreateSerializer, BookingSerializer
from django.shortcuts import redirect
from django.core.mail import EmailMultiAlternatives
class BookingViewSet(viewsets.ModelViewSet):
    """
    API endpoints for bookings.

    list:     GET  /api/bookings/         → current user's bookings
    create:   POST /api/bookings/         → create booking + get eSewa payload
    retrieve: GET  /api/bookings/{id}/    → single booking detail
    """

    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_anonymous:
            return Booking.objects.none()
        return Booking.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'create':
            return BookingCreateSerializer
        return BookingSerializer

    def create(self, request, *args, **kwargs):
        """
        Create booking then immediately return the eSewa payload.

        Flow:
          1. Validate form fields
          2. Calculate price from trek.discounted_price (falls back to price_usd)
          3. Save booking (booking_id auto-generated in model.save())
          4. Build eSewa signed payload
          5. Return booking data + eSewa payload in one response
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        trek = serializer.validated_data['trek']

        # Use discounted price if set, otherwise fall back to base USD price
        price_per_person = trek.discounted_price or trek.price_usd

        # Save booking — model.save() auto-sets booking_id and total_price
        booking = serializer.save(
            user=request.user,
            price_per_person=price_per_person,
        )
        print("Debug bokkingid:",booking.booking_id)
        print("Debug total_price:",booking.total_price)
        # Notify admin (best-effort — never crash the booking on email failure)
       
        self._send_whatsapp_notification(booking)
        print("booking_id being sent to eswa:",booking.booking_id)
        # Build eSewa payload using booking_id as transaction_uuid
        strategy = EsewaStrategy()
        payment_data = strategy.get_payment_payload(booking)

        return Response(
            {
                # booking_id so frontend can show a reference / pass to verify
                "booking_id": booking.booking_id,
                "message": "Booking created. Proceed to eSewa payment.",
                **payment_data,           # payment_method + esewa_payload
                "booking": BookingSerializer(booking).data,
            },
            status=status.HTTP_201_CREATED,
        )

    # ── Private helpers ────────────────────────────────────────

    def _send_booking_email(self, booking):
        subject = f'Booking Confirmed — {booking.booking_id} | Nepal Trek Connect'
        
        text_body = f"""
    Dear {booking.full_name},

    Your booking is confirmed!

    Booking ID:   {booking.booking_id}
    Trek:         {booking.trek.title}
    Date:         {booking.start_date}
    People:       {booking.number_of_people}
    Total:        NPR {float(booking.total_price):.2f}

    We will contact you within 24 hours with further details.

    WhatsApp: +977 9846958184
    Nepal Trek Connect
        """

        html_body = f"""
    <!DOCTYPE html>
    <html>
    <body style="font-family: Arial, sans-serif; max-width: 600px; margin: auto; padding: 20px; color: #333;">
    <div style="background: #16a34a; padding: 24px; border-radius: 8px 8px 0 0; text-align: center;">
        <h1 style="color: white; margin: 0;">✅ Booking Confirmed!</h1>
    </div>
    <div style="border: 1px solid #e5e7eb; border-top: none; padding: 24px; border-radius: 0 0 8px 8px;">
        <p>Dear <strong>{booking.full_name}</strong>,</p>
        <p>Your trek booking has been confirmed. Here are your details:</p>

        <table style="width:100%; border-collapse: collapse; margin: 16px 0;">
        <tr style="background:#f9fafb;">
            <td style="padding:10px; border:1px solid #e5e7eb; font-weight:bold;">Booking ID</td>
            <td style="padding:10px; border:1px solid #e5e7eb; font-family:monospace;">{booking.booking_id}</td>
        </tr>
        <tr>
            <td style="padding:10px; border:1px solid #e5e7eb; font-weight:bold;">Trek</td>
            <td style="padding:10px; border:1px solid #e5e7eb;">{booking.trek.title}</td>
        </tr>
        <tr style="background:#f9fafb;">
            <td style="padding:10px; border:1px solid #e5e7eb; font-weight:bold;">Start Date</td>
            <td style="padding:10px; border:1px solid #e5e7eb;">{booking.start_date}</td>
        </tr>
        <tr>
            <td style="padding:10px; border:1px solid #e5e7eb; font-weight:bold;">Number of People</td>
            <td style="padding:10px; border:1px solid #e5e7eb;">{booking.number_of_people}</td>
        </tr>
        <tr style="background:#f9fafb;">
            <td style="padding:10px; border:1px solid #e5e7eb; font-weight:bold;">Total Paid</td>
            <td style="padding:10px; border:1px solid #e5e7eb; color:#16a34a; font-weight:bold;">NPR {float(booking.total_price):.2f}</td>
        </tr>
        </table>

        <p>We will contact you within 24 hours with a detailed itinerary and packing list.</p>
        <p>For any questions, reach us on WhatsApp: <strong>+977 9846958184</strong></p>

        <div style="margin-top:24px; padding-top:16px; border-top:1px solid #e5e7eb; font-size:12px; color:#6b7280; text-align:center;">
        Nepal Trek Connect — Connecting You to the Himalayas
        </div>
    </div>
    </body>
    </html>
        """

        try:
            msg = EmailMultiAlternatives(
                subject=subject,
                body=text_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[booking.email],
            )
            msg.attach_alternative(html_body, "text/html")
            msg.send()
        except Exception as e:
            print(f"Email error: {e}")

    def _send_whatsapp_notification(self, booking):
        message = f"New Booking: {booking.booking_id} - {booking.trek.title}"
        print(f"WhatsApp notification: {message}")


class PaymentCallbackViewSet(viewsets.ViewSet):
    """
    Handles the redirect callback from eSewa after payment.

    eSewa sends: GET /api/bookings/esewa-verify/?data=<base64>
    The `data` param is a Base64-encoded JSON string.
    """

    @action(detail=False, methods=['get'], url_path='esewa-verify')
    def esewa_verify(self, request):
        encoded_data = request.query_params.get('data')
        if not encoded_data:
            return Response({'error': 'No data received from eSewa'}, status=400)

        try:
            decoded_bytes = base64.b64decode(encoded_data)
            decoded_data = json.loads(decoded_bytes.decode('utf-8'))
            print("debug esewa call back:",decoded_data)
            # Fields eSewa sends back:
            # transaction_code  — eSewa's own reference
            # status            — "COMPLETE" | "INCOMPLETE" | "PENDING"
            # transaction_uuid  — our booking_id
            status_received = decoded_data.get('status')
            booking_id = decoded_data.get('transaction_uuid')
            esewa_ref = decoded_data.get('transaction_code')
            print(f"Debug looking booking_id:'{booking_id}'")
            if status_received == "COMPLETE":
                booking = get_object_or_404(Booking, booking_id=booking_id)
                booking.status = 'confirmed'
                booking.transaction_id = esewa_ref
                booking.payment_response = decoded_data
                booking.save()
                BookingViewSet()._send_booking_email(booking)
                return redirect(f"http://localhost:3000/payment/success?booking_id={booking.booking_id}")
                
            return Response(
                {"error": f"Payment not completed. Status: {status_received}"},
                status=400,
            )

        except Exception as e:
            return Response({"error": str(e)}, status=400)