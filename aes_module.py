import base64
import hashlib
from cryptography.fernet import Fernet

def generate_key(user_key: str):
    """
    Convert user key into valid 32-byte AES key using SHA-256
    """
    hash_key = hashlib.sha256(user_key.encode()).digest()
    return base64.urlsafe_b64encode(hash_key)

def aes_encrypt(plain_text, user_key):
    key = generate_key(user_key)
    cipher = Fernet(key)
    encrypted = cipher.encrypt(plain_text.encode())
    return encrypted.decode()

def aes_decrypt(cipher_text, user_key):
    key = generate_key(user_key)
    cipher = Fernet(key)
    decrypted = cipher.decrypt(cipher_text.encode())
    return decrypted.decode()
