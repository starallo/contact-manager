#!/usr/bin/env python3
"""Generate password hashes for users.csv"""
import hashlib
import os
import base64

def generate_pbkdf2_hash(password, method='pbkdf2:sha256', iterations=1000):
    """Generate a pbkdf2 hash compatible with werkzeug"""
    salt = os.urandom(16)
    h = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, iterations)
    salt_b64 = base64.b64encode(salt).decode('ascii')
    hash_b64 = base64.b64encode(h).decode('ascii')
    return f"{method}:{iterations}${salt_b64}${hash_b64}"

password = 'pwd'
hash_value = generate_pbkdf2_hash(password)
print(f"Password hash for '{password}': {hash_value}")
