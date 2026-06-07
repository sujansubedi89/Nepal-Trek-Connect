from django.conf import settings
from .utils import generate_esewa_signature


class EsewaStrategy:
    """
    Builds the eSewa payment form payload.

    eSewa uses a form-submission model: we build all the hidden form fields
    here, and the frontend creates an actual <form> element and submits it.
    """

    def get_payment_payload(self, booking):
        conf = settings.ESEWA_SETTINGS

        # Must be exactly 2 decimal places — "100" vs "100.00" give different signatures
        amount_str = "{:.2f}".format(booking.total_price)

        # booking_id is our unique order reference — used as eSewa's transaction_uuid
        signature = generate_esewa_signature(
            total_amount=amount_str,
            transaction_uuid=booking.booking_id,
            product_code=conf["MERCHANT_ID"],
            secret_key=conf["SECRET_KEY"],
        )

        return {
            "payment_method": "eSewa",
            "esewa_payload": {
                "amount": amount_str,
                "tax_amount": "0",
                "total_amount": amount_str,
                "product_service_charge": "0",
                "product_delivery_charge": "0",
                "transaction_uuid": booking.booking_id,
                "product_code": conf["MERCHANT_ID"],
                "success_url": conf["SUCCESS_URL"],
                "failure_url": conf["FAILURE_URL"],
                "signed_field_names": "total_amount,transaction_uuid,product_code",
                "signature": signature,
                "esewa_url": conf["INITIATE_URL"],
            },
        }