import secrets
import string
from fastapi import Request

def generate_api_key(request: Request):
    key_length = 32
    alphabet = string.ascii_letters + string.digits
    api_key = ''.join(secrets.choice(alphabet) for _ in range(key_length))
    return api_key