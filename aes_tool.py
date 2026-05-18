import os
from cryptography.hazmat.primitives.ciphers import Cipher,algorithms,modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
def encrypt(plain_text, key):
    iv = os.urandom(16)
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(plain_text.encode()) + padder.finalize()
    cipher = Cipher(algorithms.AES(key),modes.CBC(iv),backend=default_backend())
    encryptor = cipher.encryptor()
    cipher_text = encryptor.update(padded_data) + encryptor.finalize()
    return iv + cipher_text
def decrypt(token, key):
    iv = token[:16]
    cipher_text = token[16:]
    cipher = Cipher(algorithms.AES(key),modes.CBC(iv),backend=default_backend())
    decryptor = cipher.decryptor()
    padded_data = decryptor.update(cipher_text) + decryptor.finalize()
    unpadder = padding.PKCS7(128).unpadder()
    data = unpadder.update(padded_data) + unpadder.finalize()
    return data.decode()
if __name__ == "__main__":
    secret_key = os.urandom(32)
    message = "Ceci est un secret pour les hackers de la séance 2"
    print(f"Message original : {message}")
    token = encrypt(message, secret_key)
    print(f"Text chiffré (hex) : {token.hex()}")
    clear_text = decrypt(token, secret_key)
    print(f"Message déchifré : {clear_text}")