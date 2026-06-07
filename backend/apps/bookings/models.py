import uuid
from django.db import models
from django.core.validators import MinValueValidator
from django.conf import settings
from apps.treks.models import Trek


class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Payment'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    ]

    # ── Reference ─────────────────────────────────────────────
    # booking_id is the human-readable reference (NTC + 8 hex chars)
    # order_code is the same value — used as eSewa's transaction_uuid
    # We keep ONE field called booking_id and alias it for eSewa.
    booking_id = models.CharField(max_length=50, unique=True, blank=True)

    # ── Relations ──────────────────────────────────────────────
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bookings',
    )
    trek = models.ForeignKey(
        Trek,
        on_delete=models.PROTECT,
        related_name='bookings',
    )

    # ── Customer Details ───────────────────────────────────────
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    country_code = models.CharField(max_length=5, default='+977')
    whatsapp_number = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, blank=True)

    # ── Booking Details ────────────────────────────────────────
    number_of_people = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    start_date = models.DateField()
    special_requests = models.TextField(blank=True)

    # ── Pricing ────────────────────────────────────────────────
    price_per_person = models.DecimalField(max_digits=10, decimal_places=2)
    # total_price is computed in save(); stored for querying/display
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    commission_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    # ── Status ─────────────────────────────────────────────────
    # Named `status` to match admin, serializers, and frontend expectations
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    # ── Payment ────────────────────────────────────────────────
    transaction_id = models.CharField(max_length=100, null=True, blank=True)
    payment_response = models.JSONField(null=True, blank=True)

    # ── Timestamps ─────────────────────────────────────────────
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    # booking_id doubles as eSewa's transaction_uuid
    @property
    def order_code(self):
        return self.booking_id

    def save(self, *args, **kwargs):
        if not self.booking_id:
            self.booking_id = f"NTC{uuid.uuid4().hex[:8].upper()}"
        self.total_price = self.price_per_person * self.number_of_people
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.booking_id} - {self.trek.title}"