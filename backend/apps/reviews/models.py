from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.treks.models import Trek

class Review(models.Model):
    """Trek review and rating model"""
    
    # Relations
    trek = models.ForeignKey(Trek, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    
    # Review Details
    rating = models.PositiveIntegerField(validators=[MinValueValidator(4), MaxValueValidator(5)])
    title = models.CharField(max_length=255)
    comment = models.TextField()
    
    # Images
    image1 = models.ImageField(upload_to='reviews/', blank=True, null=True)
    image2 = models.ImageField(upload_to='reviews/', blank=True, null=True)
    image3 = models.ImageField(upload_to='reviews/', blank=True, null=True)
    
    # Status
    is_verified = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ['trek', 'user']
    
    def __str__(self):
        return f"{self.user.email} - {self.trek.title} - {self.rating}★"
