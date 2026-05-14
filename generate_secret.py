#!/usr/bin/env python
import secrets
import string

# Generate a secure Django SECRET_KEY
alphabet = string.ascii_letters + string.digits + string.punctuation
secret_key = ''.join(secrets.choice(alphabet) for _ in range(50))

print("Generated Django SECRET_KEY:")
print(secret_key)
print("\nAdd this to your .env file:")
print(f"SECRET_KEY={secret_key}")