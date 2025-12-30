from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator


from django.utils.translation import gettext_lazy as _
from decimal import Decimal
class Trek(models.Model):
    """Main Trek Package Model"""
    
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('easy_moderate', 'Easy to Moderate'),
        ('moderate', 'Moderate'),
        ('moderate_challenging', 'Moderate to Challenging'),
        ('challenging', 'Challenging'),
        ('very_challenging', 'Very Challenging'),
    ]
    
    SEASON_CHOICES = [
        ('all_year', 'All Year Round'),
        ('spring_autumn', 'Spring & Autumn (Best)'),
        ('march_may', 'March-May'),
        ('september_november', 'September-November'),
        ('march_november', 'March-November'),
    ]
    
    # Basic Information
    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=300, unique=True, blank=True)
    short_description = models.TextField(max_length=500)
    long_description = models.TextField()
    
    # Location
    location = models.CharField(max_length=255, help_text="e.g., Pokhara, Annapurna Region, Himalayas")
    start_point = models.CharField(max_length=100, default='Pokhara')
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    
    # Trek Details
    duration_days = models.PositiveIntegerField()
    duration_nights = models.PositiveIntegerField()
    difficulty = models.CharField(max_length=30, choices=DIFFICULTY_CHOICES)
    max_altitude = models.PositiveIntegerField(help_text="In meters")
    max_altitude_feet = models.PositiveIntegerField(help_text="In feet")
    best_season = models.CharField(max_length=50, choices=SEASON_CHOICES)
    
    # Pricing
    price_usd = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    discount_percentage = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(100)])
    
    # Images
    hero_image = models.ImageField(upload_to='trek_images/hero/', blank=True, null=True)
    image_keywords = models.TextField(help_text="Comma-separated keywords for images", blank=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    is_popular = models.BooleanField(default=False)
    
    # SEO Fields
    meta_title = models.CharField(max_length=255, blank=True)
    meta_description = models.TextField(max_length=500, blank=True)
    meta_keywords = models.TextField(blank=True)
    
    # Stats
    total_bookings = models.PositiveIntegerField(default=0)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    total_reviews = models.PositiveIntegerField(default=0)
    views_count = models.PositiveIntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-is_featured', '-is_popular', '-created_at']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['difficulty']),
            models.Index(fields=['price_usd']),
        ]
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if not self.meta_title:
            self.meta_title = f"{self.title} | Nepal Trek Connect"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    
    @property
    def discounted_price(self):
        if self.discount_percentage > 0:
            return self.price_usd * (1 - self.discount_percentage /Decimal( 100))
        return self.price_usd


class TrekImage(models.Model):
    """Additional gallery images for treks"""
    trek = models.ForeignKey(Trek,related_name='gallery_images' ,on_delete=models.CASCADE )
    image = models.ImageField(
       
        upload_to='trek_images/gallery/%Y/%m/' # Good practice to use a dynamic path
    )
    caption = models.CharField(max_length=255, blank=True,null=True)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['trek', 'order']
       

class Itinerary(models.Model):
    """Daily itinerary for each trek"""
    trek = models.ForeignKey(Trek, on_delete=models.CASCADE, related_name='itinerary')
    day_number = models.PositiveIntegerField()
    title = models.CharField(max_length=255)
    description = models.TextField()
    altitude = models.CharField(max_length=100, blank=True)
    trekking_hours = models.CharField(max_length=50, blank=True)
    accommodation = models.CharField(max_length=100, blank=True)
    meals_included = models.CharField(max_length=100, default='Breakfast, Lunch, Dinner')
    
    class Meta:
        ordering = ['day_number']
        unique_together = ['trek', 'day_number']
    
    def __str__(self):
        return f"Day {self.day_number}: {self.title}"


class IncludedItem(models.Model):
    """Items included in trek package"""
    trek = models.ForeignKey(Trek, on_delete=models.CASCADE, related_name='included_items')
    item = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.item


class ExcludedItem(models.Model):
    """Items excluded from trek package"""
    trek = models.ForeignKey(Trek, on_delete=models.CASCADE, related_name='excluded_items')
    item = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.item


class MapCoordinate(models.Model):
    """Map waypoints for trek route"""
    trek = models.ForeignKey(Trek, on_delete=models.CASCADE, related_name='map_coordinates')
    name = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.trek.title} - {self.name}"

# Create your models here.
