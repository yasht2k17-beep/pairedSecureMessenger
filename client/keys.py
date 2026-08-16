from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey
from cryptography.hazmat.primitives import serialization
import os 

class KeyManager:
    def __init__(self,username):
        self.username=username
        self.keyDir="keys"

        os.makedirs(self.keyDir,exist_ok=True)

        self.privatePath=os.path.join(self.keyDir,f"{username}_private.key")

    def genKeyPair(self):
        privateKey=X25519PrivateKey.generate()
        self.savePrivateKey(privateKey)

        return privateKey

    def savePrivateKey(self,privateKey):
        keyBytes=privateKey.private_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PrivateFormat.Raw,
            encryption_algorithm=serialization.NoEncryption()
        )

        with open(self.privatePath,"wb") as file:
            file.write(keyBytes)

    def loadPrivateKey(self):
        if not os.path.exists(self.privatePath):
            return None
        with open(self.privatePath,"rb") as file:
            keyBytes=file.read()

        return X25519PrivateKey.from_private_bytes(keyBytes)

    def getPrivateKey(self):
        privateKey=self.loadPrivateKey()

        if privateKey is None:
            privateKey=self.genKeyPair()

        return privateKey

    def getPublicKey(self,privateKey):
        return privateKey.public_key()