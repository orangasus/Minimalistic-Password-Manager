import bcrypt
from cryptography.fernet import Fernet

def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password

def check_if_password_matches_hashed(hashed_password, user_password):
    return bcrypt.checkpw(user_password.encode(), hashed_password)

def encrypt_password(password, user_key):
    return Fernet(user_key).encrypt(password.encode())

def decrypt_password(encrypted_password, user_key):
    return Fernet(user_key).decrypt(encrypted_password).decode()

def generate_user_key():
    return Fernet.generate_key()
