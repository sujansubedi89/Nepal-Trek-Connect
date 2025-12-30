from django.db import models

class SEOMetadata(models.Model):
    """SEO metadata for dynamic pages"""
    page_type = models.CharField(max_length=50)  # homepage, trek_list, about, etc.
    page_identifier = models.CharField(max_length=255, blank=True)  # trek slug, etc.
    
    meta_title = models.CharField(max_length=255)
    meta_description = models.TextField(max_length=500)
    meta_keywords = models.TextField()
    canonical_url = models.URLField(blank=True)
    
    og_title = models.CharField(max_length=255, blank=True)
    og_description = models.TextField(max_length=500, blank=True)
    og_image = models.URLField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['page_type', 'page_identifier']
    
    def __str__(self):
        return f"{self.page_type} - {self.meta_title}"