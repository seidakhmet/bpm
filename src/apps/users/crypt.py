import base64
from typing import Tuple
from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey.RSA import RsaKey
from Crypto.Hash import SHA256


def newkeys(keysize: int) -> Tuple[RsaKey, RsaKey]:
    random_generator = Random.new().read
    key = RSA.generate(keysize, random_generator)
    private, public = key, key.publickey()
    return public, private


def encrypt(message: str, public_key: RsaKey):
    cipher = PKCS1_OAEP.new(public_key, hashAlgo=SHA256)  # type: ignore
    ciphertext = cipher.encrypt(message.encode())
    return base64.b64encode(ciphertext)


def decrypt(ciphertext: str, private_key: RsaKey):
    cipher = PKCS1_OAEP.new(private_key, hashAlgo=SHA256)  # type: ignore
    ciphertext = base64.b64decode(ciphertext)
    return cipher.decrypt(ciphertext)
