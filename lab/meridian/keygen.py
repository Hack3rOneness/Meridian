"""Generate the portal's RSA keypair (run once at build)."""
import os
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

os.makedirs("keys", exist_ok=True)
k = rsa.generate_private_key(public_exponent=65537, key_size=2048)
open("keys/private.pem", "wb").write(k.private_bytes(
    serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8,
    serialization.NoEncryption()))
open("keys/public.pem", "wb").write(k.public_key().public_bytes(
    serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo))
print("keys generated")
