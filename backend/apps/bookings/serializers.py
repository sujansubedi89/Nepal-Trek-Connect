from rest_framework import serializers
from .models import Booking
from apps.treks.serializers import TrekListSerializer

class BookingSerializer(serializers.ModelSerializer):
    trek_details = TrekListSerializer(source='trek', read_only=True)
    
    class Meta:
        model = Booking
        fields = ['id', 'booking_id', 'trek', 'trek_details', 'full_name', 'email', 
                  'phone', 'country_code', 'whatsapp_number', 'country', 
                  'number_of_people', 'start_date', 'special_requests', 
                  'price_per_person', 'total_price', 'status', 'created_at']
        read_only_fields = ['booking_id', 'user', 'total_price', 'status']

class BookingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['trek', 'full_name', 'email', 'phone', 'country_code', 
                  'whatsapp_number', 'country', 'number_of_people', 'start_date', 
                  'special_requests']
