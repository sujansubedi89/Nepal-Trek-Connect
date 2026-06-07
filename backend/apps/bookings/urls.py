from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import BookingViewSet,PaymentCallbackViewSet

router = SimpleRouter()
router.register(r'', BookingViewSet, basename='booking')

urlpatterns = [
    path('esewa-verify/',PaymentCallbackViewSet.as_view({'get':'esewa_verify'}),name='esewa-verify'),
    path('', include(router.urls)),
    
]
