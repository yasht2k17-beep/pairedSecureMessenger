from client.api_client import APIClient
from client.keys import KeyManager


def setupUser(username, password):

    client = APIClient()

    keyManager = KeyManager(username)

    privateKey = keyManager.getPrivateKey()

    publicKey = keyManager.getPublicKey(
        privateKey
    )

    publicKeyHex = publicKey.public_bytes_raw().hex()

    result = client.register(
        username,
        password,
        publicKeyHex
    )

    print(
        f"{username} register:",
        result
    )

    return client


# --------------------------------
# Create clients
# --------------------------------

alice = setupUser(
    "pairAlice2",
    "alice123"
)

bob = setupUser(
    "pairBob2",
    "bob123"
)


# --------------------------------
# Login
# --------------------------------

print("\nAlice login:")

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


# --------------------------------
# Test public key retrieval
# --------------------------------

print("\nBob's public key:")

print(
    alice.getPublicKey(
        "pairBob2"
    )
)


print("\nAlice's public key:")

print(
    bob.getPublicKey(
        "pairAlice2"
    )
)