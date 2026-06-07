import hmac
import hashlib
import base64

def generate_esewa_signature(total_amount, transaction_uuid, product_code, secret_key):
    """
    Generate HMAC-SHA256 signature for eSewa epay v2.
    
    CRITICAL FORMAT RULES:
    - Fields are separated by commas with NO spaces
    - Fields must be in this exact order: total_amount, transaction_uuid, product_code
    - Each field is in key=value format
    - The output is Base64-encoded (not hex)
    
    Args:
        total_amount:     String like "1000.00" — must match the form field exactly
        transaction_uuid: Your order_code (e.g., "ABC123")
        product_code:     Your MERCHANT_ID (e.g., "EPAYTEST")
        secret_key:       Your eSewa secret key
    
    Returns:
        Base64-encoded HMAC-SHA256 signature string
    """
    # Build the data string — DO NOT add spaces after commas
    data = f"total_amount={total_amount},transaction_uuid={transaction_uuid},product_code={product_code}"
    
    # Encode both to bytes
    secret_key_bytes = secret_key.encode('utf-8')
    data_bytes = data.encode('utf-8')
    
    # Create the HMAC-SHA256 hash
    hash_obj = hmac.new(secret_key_bytes, data_bytes, hashlib.sha256).digest()
    
    # Return as Base64 string
    return base64.b64encode(hash_obj).decode('utf-8')