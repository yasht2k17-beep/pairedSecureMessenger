from database import Database
from server.auth import Auth
from server.pair import PairManager
from server.message import Message
from client.crypto import Crypto


# =========================
# Database
# =========================

db = Database()


# =========================
# Authentication
# =========================

auth = Auth(db)


# =========================
# Pairing
# =========================

pair = PairManager(db)


# =========================
# X25519 Key Exchange
# =========================

alicePrivate, alicePublic = Crypto.genKeyPair()
bobPrivate, bobPublic = Crypto.genKeyPair()


aliceSecret = Crypto.genSharedSecret(
    alicePrivate,
    bobPublic
)

bobSecret = Crypto.genSharedSecret(
    bobPrivate,
    alicePublic
)


print(
    "Shared secrets match:",
    aliceSecret == bobSecret
)


# =========================
# Derive AES Keys
# =========================

aliceKey = Crypto.deriveKey(aliceSecret)
bobKey = Crypto.deriveKey(bobSecret)


print(
    "AES keys match:",
    aliceKey == bobKey
)


# =========================
# Create Crypto Objects
# =========================

aliceCrypto = Crypto(aliceKey)
bobCrypto = Crypto(bobKey)


# =========================
# Message Managers
# =========================

aliceMessages = Message(
    db,
    pair
)

bobMessages = Message(
    db,
    pair
)


# =========================
# Register Users
# =========================

print(
    "Register Alice:",
    auth.register("Alice", "alice123")
)

print(
    "Register Bob:",
    auth.register("Bob", "bob123")
)


# =========================
# Pair Users
# =========================

print(
    "Pair request:",
    pair.requestPair("Alice", "Bob")
)

print(
    "Accept request:",
    pair.respondToPair(
        "Bob",
        "Alice",
        "accept"
    )
)


# =========================
# Send Messages
# =========================

print(
    "Send 1:",
    aliceMessages.send(
        "Alice",
        "Bob",
        "Hello Bob!"
    )
)

print(
    "Send 2:",
    bobMessages.send(
        "Bob",
        "Alice",
        "Hello Alice!"
    )
)


# =========================
# Retrieve Conversation
# =========================

conversation = bobMessages.getMessages(
    "Alice",
    "Bob"
)


print("\nConversation")
print("----------------")

for message in conversation:

    print(
        f"[{message['timestamp']}] "
        f"{message['sender']}: "
        f"{message['message']}"
    )