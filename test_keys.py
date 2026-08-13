from database import Database
from auth import Auth


db = Database()
auth = Auth(db)

print(
    "Register Alice:",
    auth.register("Alice", "alice123")
)

user = db.fetchOne(
    "SELECT username, public_key FROM users WHERE username=?",
    ("Alice",)
)

print("Username:", user[0])
print("Public key:", user[1])