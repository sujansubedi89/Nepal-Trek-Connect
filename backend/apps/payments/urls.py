from django.urls import path
from .views import InitiateESewaPaymentView, VerifyESewaPaymentView

urlpatterns = [
    # eSewa
    path('esewa/initiate/', InitiateESewaPaymentView.as_view(), name='esewa_initiate'),
    path('esewa/verify/', VerifyESewaPaymentView.as_view(), name='esewa_verify'),
]