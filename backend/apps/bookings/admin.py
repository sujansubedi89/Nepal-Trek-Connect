from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['booking_id', 'user', 'trek', 'start_date', 'number_of_people', 'total_price', 'status', 'created_at']
    list_filter = ['status', 'created_at', 'start_date']
    search_fields = ['booking_id', 'user__email', 'trek__title', 'full_name', 'email']
    readonly_fields = ['booking_id', 'created_at', 'updated_at', 'total_price']
    
    fieldsets = (
        ('Booking Information', {
            'fields': ('booking_id', 'user', 'trek', 'status')
        }),
        ('Customer Details', {
            'fields': ('full_name', 'email', 'phone', 'country_code', 'whatsapp_number', 'country')
        }),
        ('Trip Details', {
            'fields': ('number_of_people', 'start_date', 'special_requests')
        }),
        ('Pricing', {
            'fields': ('price_per_person', 'total_price', 'commission_amount')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'confirmed_at')
        }),
    )
