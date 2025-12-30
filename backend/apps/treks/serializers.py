from rest_framework import serializers
from .models import Trek, TrekImage, Itinerary, IncludedItem, ExcludedItem, MapCoordinate

class TrekImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrekImage
        fields = ['id', 'image', 'caption', 'order']

class ItinerarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Itinerary
        fields = ['id', 'day_number', 'title', 'description', 'altitude', 
                  'trekking_hours', 'accommodation', 'meals_included']

class IncludedItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = IncludedItem
        fields = ['id', 'item']

class ExcludedItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExcludedItem
        fields = ['id', 'item']

class MapCoordinateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MapCoordinate
        fields = ['id', 'name', 'latitude', 'longitude']

class TrekListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for trek listing"""
    discounted_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = Trek
        fields = ['id', 'title', 'slug', 'short_description', 'location', 
                  'duration_days', 'duration_nights', 'difficulty', 'max_altitude',
                  'price_usd', 'discount_percentage', 'discounted_price',
                  'hero_image', 'is_featured', 'is_popular', 'average_rating', 
                  'total_reviews', 'best_season']

class TrekDetailSerializer(serializers.ModelSerializer):
    """Complete serializer for trek detail page"""
    gallery = TrekImageSerializer(source='gallery_images',many=True, read_only=True)
    itinerary = ItinerarySerializer(many=True, read_only=True)
    included_items = IncludedItemSerializer(many=True, read_only=True)
    excluded_items = ExcludedItemSerializer(many=True, read_only=True)
    map_coordinates = MapCoordinateSerializer(many=True, read_only=True)
    discounted_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = Trek
        fields = '__all__'
