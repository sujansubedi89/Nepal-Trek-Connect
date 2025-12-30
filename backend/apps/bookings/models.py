from django.db import models
from django.core.validators import MinValueValidator

from django.conf import settings
from apps.treks.models import Trek

class Booking(models.Model):
    """Trek booking/reservation model"""
    
    STATUS_CHOICES = [
        ('pending', 'Pending Payment'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    ]
    
    # Reference
    booking_id = models.CharField(max_length=50, unique=True, editable=False)
    
    # Relations
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    trek = models.ForeignKey(Trek, on_delete=models.PROTECT, related_name='bookings')
    
    # Customer Details
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    country_code = models.CharField(max_length=5)
    whatsapp_number = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    
    # Booking Details
    number_of_people = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    start_date = models.DateField()
    special_requests = models.TextField(blank=True)
    
    # Pricing
    price_per_person = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    commission_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def save(self, *args, **kwargs):
        if not self.booking_id:
            import uuid
            self.booking_id = f"NTC{uuid.uuid4().hex[:8].upper()}"
        self.total_price = self.price_per_person * self.number_of_people
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.booking_id} - {self.trek.title}"