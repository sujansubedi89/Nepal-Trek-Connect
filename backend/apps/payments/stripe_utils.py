import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_payment_intent(amount, currency='usd', metadata=None):
    """Create a Stripe Payment Intent"""
    try:
        intent = stripe.PaymentIntent.create(
            amount=int(amount * 100),  # Convert to cents
            currency=currency,
            metadata=metadata or {},
            automatic_payment_methods={'enabled': True}
        )
        return intent
    except stripe.error.StripeError as e:
        raise Exception(str(e))

def create_refund(payment_intent_id, amount=None):
    """Create a refund for a payment"""
    try:
        refund = stripe.Refund.create(
            payment_intent=payment_intent_id,
            amount=int(amount * 100) if amount else None
        )
        return refund
    except stripe.error.StripeError as e:
        raise Exception(str(e))