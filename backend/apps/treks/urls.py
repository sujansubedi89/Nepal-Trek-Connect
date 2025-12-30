from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TrekViewSet

router = DefaultRouter()
router.register(r'', TrekViewSet, basename='trek')

urlpatterns = [
    path('', include(router.urls)),
]