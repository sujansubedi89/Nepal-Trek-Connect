import hmac
import hashlib
import base64

def generate_esewa_signature(total_amount, transaction_uuid, product_code, secret_key):
    """
    CRITICAL FORMAT RULES (from eSewa docs):
    - NO spaces after commas
    - Exact order: total_amount, transaction_uuid, product_code
    - Amount must be formatted as "854.05" — must match form field exactly
    """
    data = f"total_amount={total_amount},transaction_uuid={transaction_uuid},product_code={product_code}"
    
    secret_key_bytes = secret_key.encode('utf-8')
    data_bytes = data.encode('utf-8')
    
    hash_obj = hmac.new(secret_key_bytes, data_bytes, hashlib.sha256).digest()
    return base64.b64encode(hash_obj).decode('utf-8')