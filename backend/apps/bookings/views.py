from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated ,AllowAny
from django.core.mail import send_mail
from django.conf import settings
from .models import Booking
from .serializers import BookingSerializer, BookingCreateSerializer
from apps.treks.models import Trek

class BookingViewSet(viewsets.ModelViewSet):
    """
    API endpoint for bookings
    
    list: Get user's bookings
    create: Create new booking
    retrieve: Get booking details
    """
    serializer_class = BookingSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        """Return bookings for current user"""
        return Booking.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.action == 'create':
            return BookingCreateSerializer
        return BookingSerializer
    
    def create(self, request, *args, **kwargs):
        """Create new booking"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Get trek and calculate price
        trek = serializer.validated_data['trek']
        num_people = serializer.validated_data['number_of_people']
        price_per_person = trek.discounted_price
        
        # Create booking
        booking = serializer.save(
            user=request.user,
            price_per_person=price_per_person
        )
        
        # Send confirmation email (console for development)
        self.send_booking_email(booking)
        
        # Send WhatsApp notification (implementation depends on service)
        self.send_whatsapp_notification(booking)
        
        return Response(
            BookingSerializer(booking).data,
            status=status.HTTP_201_CREATED
        )
    
    def send_booking_email(self, booking):
        """Send booking confirmation email"""
        subject = f'Booking Confirmation - {booking.booking_id}'
        message = f"""
        Dear {booking.full_name},
        
        Your booking for {booking.trek.title} has been created successfully!
        
        Booking ID: {booking.booking_id}
        Trek: {booking.trek.title}
        Date: {booking.start_date}
        Number of People: {booking.number_of_people}
        Total Price: ${booking.total_price}
        
        Please proceed to payment to confirm your booking.
        
        Contact: +977 9846958184
        WhatsApp: +977 9846958184
        
        Best regards,
        Nepal Trek Connect
        """
        
        try:
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [booking.email],
                fail_silently=False,
            )
        except Exception as e:
            print(f"Email error: {e}")
    
    def send_whatsapp_notification(self, booking):
        """Send WhatsApp notification to admin"""
        # Implementation using WhatsApp Business API
        # For now, just log
        message = f"New Booking: {booking.booking_id} - {booking.trek.title}"
        print(f"WhatsApp notification: {message}")
