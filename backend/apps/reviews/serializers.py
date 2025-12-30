from rest_framework import serializers
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Review
        fields = ['id', 'user_name', 'rating', 'title', 'comment', 
                  'image1', 'image2', 'image3', 'is_verified', 'created_at']
        read_only_fields = ['user_name', 'is_verified']
    
    def get_user_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"
