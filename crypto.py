from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.asymmetric.x25519 import (
    X25519PrivateKey
    )
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
import os

class Crypto:
    def __init__(self,key):
        self.key=key
        self.aes=AESGCM(self.key)

    def encrypt(self,msg):
        nonce=os.urandom(12)
        encrypted=self.aes.encrypt(nonce,msg.encode(),None)

        return nonce+encrypted

    def decrypt(self,encrypted):
        nonce=encrypted[:12]
        cipher=encrypted[12:]

        decrypted=self.aes.decrypt(nonce,cipher,None)

        return decrypted.decode()

    @staticmethod
    def genKeyPair():
        privateKey=X25519PrivateKey.generate()
        publicKey=privateKey.public_key()

        return privateKey,publicKey

    @staticmethod
    def genSharedSecret(privateKey,publicKey):
        return privateKey.exchange(publicKey)

    @staticmethod
    def deriveKey(sharedSecret):
        return HKDF(algorithm=hashes.SHA256(),length=32,salt=None,info=b"paired",).derive(sharedSecret)

    def encryptBytes(self,data):
        nonce=os.urandom(12)

        encrypted=self.aes.encrypt(nonce,data,None)

        return nonce+encrypted

    def decryptBytes(self,encrypted):
        nonce=encrypted[:12]
        cipher=encrypted[12:]

        decrypted=self.aes.decrypt(nonce,cipher,None)

        return decrypted