import base64

from client.api_client import APIClient
from client.keys import KeyManager
from client.crypto import Crypto

from cryptography.hazmat.primitives.asymmetric.x25519 import (
    X25519PublicKey
)


# --------------------------------
# Clients
# --------------------------------

alice = APIClient()
bob = APIClient()


# --------------------------------
# Login
# --------------------------------

print("Alice login:")

print(
    alice.login(
        "pairAlice2",
        "alice123"
    )
)


print("\nBob login:")

print(
    bob.login(
        "pairBob2",
        "bob123"
    )
)

print("\nPairing:")

print(
    alice.requestPair("pairBob2")
)

print(
    bob.respondPair(
        "pairAlice2",
        "accept"
    )
)
# --------------------------------
# Load private keys
# --------------------------------

aliceKeys = KeyManager("pairAlice2")
bobKeys = KeyManager("pairBob2")

alicePrivate = aliceKeys.getPrivateKey()
bobPrivate = bobKeys.getPrivateKey()


# --------------------------------
# Get public keys
# --------------------------------

bobPublicHex = alice.getPublicKey(
    "pairBob2"
)["publicKey"]

alicePublicHex = bob.getPublicKey(
    "pairAlice2"
)["publicKey"]


bobPublic = X25519PublicKey.from_public_bytes(
    bytes.fromhex(bobPublicHex)
)

alicePublic = X25519PublicKey.from_public_bytes(
    bytes.fromhex(alicePublicHex)
)


# --------------------------------
# Derive shared keys
# --------------------------------

aliceSecret = Crypto.genSharedSecret(
    alicePrivate,
    bobPublic
)

aliceKey = Crypto.deriveKey(
    aliceSecret
)


bobSecret = Crypto.genSharedSecret(
    bobPrivate,
    alicePublic
)

bobKey = Crypto.deriveKey(
    bobSecret
)


print("\nKeys match:",
      aliceKey == bobKey)


# --------------------------------
# Alice encrypts
# --------------------------------

aliceCrypto = Crypto(aliceKey)

encrypted = aliceCrypto.encrypt(
    "Hello Bob! This is encrypted."
)

encryptedBase64 = base64.b64encode(
    encrypted
).decode()


print("\nEncrypted message:")
print(encryptedBase64)


# --------------------------------
# Send to server
# --------------------------------

print("\nSending:")

print(
    alice.sendMessage(
        "pairBob2",
        encryptedBase64
    )
)


# --------------------------------
# Bob retrieves messages
# --------------------------------

print("\nBob retrieves:")

result = bob.getMessages(
    "pairAlice2"
)

print(result)


# --------------------------------
# Bob decrypts latest message
# --------------------------------

encryptedReceived = result["messages"][-1]["message"]

encryptedBytes = base64.b64decode(
    encryptedReceived
)

bobCrypto = Crypto(bobKey)

decrypted = bobCrypto.decrypt(
    encryptedBytes
)

print("\nDecrypted message:")
print(decrypted)