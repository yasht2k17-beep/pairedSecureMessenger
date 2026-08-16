from client.api_client import APIClient
from client.keys import KeyManager
from client.crypto import Crypto

from cryptography.hazmat.primitives.asymmetric.x25519 import (
    X25519PublicKey
)


alice = APIClient()
bob = APIClient()


# Login
alice.login(
    "pairAlice2",
    "alice123"
)

bob.login(
    "pairBob2",
    "bob123"
)


# Load private keys
aliceKeys = KeyManager("pairAlice2")
bobKeys = KeyManager("pairBob2")

alicePrivate = aliceKeys.getPrivateKey()
bobPrivate = bobKeys.getPrivateKey()


# Get public keys from server
bobPublicHex = alice.getPublicKey(
    "pairBob2"
)["publicKey"]

alicePublicHex = bob.getPublicKey(
    "pairAlice2"
)["publicKey"]


# Convert hex → X25519 public keys
bobPublic = X25519PublicKey.from_public_bytes(
    bytes.fromhex(bobPublicHex)
)

alicePublic = X25519PublicKey.from_public_bytes(
    bytes.fromhex(alicePublicHex)
)


# Alice derives key
aliceSharedSecret = Crypto.genSharedSecret(
    alicePrivate,
    bobPublic
)

aliceAESKey = Crypto.deriveKey(
    aliceSharedSecret
)


# Bob derives key
bobSharedSecret = Crypto.genSharedSecret(
    bobPrivate,
    alicePublic
)

bobAESKey = Crypto.deriveKey(
    bobSharedSecret
)


print("Shared secrets match:",
      aliceSharedSecret == bobSharedSecret)

print("AES keys match:",
      aliceAESKey == bobAESKey)

print("AES key:", aliceAESKey.hex())