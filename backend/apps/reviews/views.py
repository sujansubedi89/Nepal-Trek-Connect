from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Review
from .serializers import ReviewSerializer
from apps.treks.models import Trek

class ReviewViewSet(viewsets.ModelViewSet):
    """
    API endpoint for trek reviews
    
    create: Submit new review (authenticated users only)
    list: Get all approved reviews
    """
    serializer_class = ReviewSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated()]
        return []
    
    def get_queryset(self):
        queryset = Review.objects.filter(is_approved=True)
        trek_id = self.request.query_params.get('trek_id', None)
        if trek_id:
            queryset = queryset.filter(trek_id=trek_id)
        return queryset
    
    def create(self, request, *args, **kwargs):
        """Create new review"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Check if user already reviewed this trek
        trek_id = request.data.get('trek')
        if Review.objects.filter(user=request.user, trek_id=trek_id).exists():
            return Response(
                {'error': 'You have already reviewed this trek'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create review
        review = serializer.save(user=request.user)
        
        # Update trek rating
        self.update_trek_rating(review.trek)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update_trek_rating(self, trek):
        """Recalculate trek average rating"""
        reviews = Review.objects.filter(trek=trek, is_approved=True)
        if reviews.exists():
            avg_rating = sum(r.rating for r in reviews) / reviews.count()
            trek.average_rating = round(avg_rating, 2)
            trek.total_reviews = reviews.count()
            trek.save(update_fields=['average_rating', 'total_reviews'])