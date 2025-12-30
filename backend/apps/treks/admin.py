
from django.contrib import admin
from .models import Trek, TrekImage, Itinerary, IncludedItem, ExcludedItem, MapCoordinate

class TrekImageInline(admin.TabularInline):
    model = TrekImage
    extra = 1

class ItineraryInline(admin.TabularInline):
    model = Itinerary
    extra = 1

class IncludedItemInline(admin.TabularInline):
    model = IncludedItem
    extra = 1

class ExcludedItemInline(admin.TabularInline):
    model = ExcludedItem
    extra = 1

class MapCoordinateInline(admin.TabularInline):
    model = MapCoordinate
    extra = 1

@admin.register(Trek)
class TrekAdmin(admin.ModelAdmin):
    list_display = ['title', 'difficulty', 'duration_days', 'price_usd', 'is_featured', 'is_active', 'total_bookings']
    list_filter = ['difficulty', 'is_featured', 'is_popular', 'is_active', 'best_season']
    search_fields = ['title', 'location', 'short_description']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [TrekImageInline, ItineraryInline, IncludedItemInline, ExcludedItemInline, MapCoordinateInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'short_description', 'long_description', 'hero_image', 'image_keywords')
        }),
        ('Location', {
            'fields': ('location', 'start_point', 'latitude', 'longitude')
        }),
        ('Trek Details', {
            'fields': ('duration_days', 'duration_nights', 'difficulty', 'max_altitude', 'max_altitude_feet', 'best_season')
        }),
        ('Pricing', {
            'fields': ('price_usd', 'discount_percentage')
        }),
        ('Status', {
            'fields': ('is_active', 'is_featured', 'is_popular')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        }),
        ('Statistics', {
            'fields': ('total_bookings', 'average_rating', 'total_reviews', 'views_count'),
            'classes': ('collapse',)
        }),
    )
