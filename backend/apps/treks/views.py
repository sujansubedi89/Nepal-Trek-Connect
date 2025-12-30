from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.db.models import Q
from .models import Trek
from .serializers import TrekListSerializer, TrekDetailSerializer
from apps.reviews.models import Review
from apps.reviews.serializers import ReviewSerializer

class TrekViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for trekking packages
    
    list: Get all active treks with filtering and search
    retrieve: Get single trek details by slug
    """
    queryset = Trek.objects.filter(is_active=True)
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'
    
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'location', 'short_description']
    ordering_fields = ['price_usd', 'duration_days', 'average_rating', 'created_at']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return TrekDetailSerializer
        return TrekListSerializer
    
    def retrieve(self, request, *args, **kwargs):
        """Get trek detail and increment view count"""
        instance = self.get_object()
        instance.views_count += 1
        instance.save(update_fields=['views_count'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    def get_queryset(self):
        """Apply custom filters"""
        queryset = super().get_queryset()
        
        # Filter by difficulty
        difficulty = self.request.query_params.get('difficulty', None)
        if difficulty:
            queryset = queryset.filter(difficulty=difficulty)
        
        # Filter by duration
        min_days = self.request.query_params.get('min_days', None)
        max_days = self.request.query_params.get('max_days', None)
        if min_days:
            queryset = queryset.filter(duration_days__gte=min_days)
        if max_days:
            queryset = queryset.filter(duration_days__lte=max_days)
        
        # Filter by price
        min_price = self.request.query_params.get('min_price', None)
        max_price = self.request.query_params.get('max_price', None)
        if min_price:
            queryset = queryset.filter(price_usd__gte=min_price)
        if max_price:
            queryset = queryset.filter(price_usd__lte=max_price)
        
        # Filter by location keyword
        location = self.request.query_params.get('location', None)
        if location:
            queryset = queryset.filter(location__icontains=location)
        
        # Show only featured
        featured = self.request.query_params.get('featured', None)
        if featured == 'true':
            queryset = queryset.filter(is_featured=True)
        
        # Show only popular
        popular = self.request.query_params.get('popular', None)
        if popular == 'true':
            queryset = queryset.filter(is_popular=True)
        
        return queryset
    
    @action(detail=True, methods=['get'])
    def reviews(self, request, slug=None):
        """Get reviews for a trek"""
        trek = self.get_object()
        reviews = Review.objects.filter(trek=trek, is_approved=True)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)