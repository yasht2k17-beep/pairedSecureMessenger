import os

from database import Database
from auth import Auth
from pair import PairManager
from filemanager import FileManager


# =========================
# Database
# =========================

db = Database()

auth = Auth(db)
pair = PairManager(db)
files = FileManager(db, pair)


# =========================
# Register users
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
# Pair users
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
# Create test file
# =========================

with open("test.txt", "w") as file:
    file.write("This is a secret file from Alice!")


# =========================
# Send file
# =========================

print(
    "Send file:",
    files.sendFile(
        "Alice",
        "Bob",
        "test.txt"
    )
)


# =========================
# List files
# =========================

fileList = files.getFiles(
    "Bob",
    "Alice"
)

print("\nFiles")
print("----------------")

for file in fileList:

    print(
        "ID:", file[0],
        "| Sender:", file[1],
        "| Receiver:", file[2],
        "| Name:", file[3],
        "| Time:", file[4]
    )


# =========================
# Download file
# =========================

if fileList:

    fileID = fileList[0][0]

    outputPath = files.downloadFile(
        fileID,
        "Bob",
        "Alice"
    )

    print(
        "\nDownloaded:",
        outputPath
    )


# =========================
# Verify
# =========================

if outputPath:

    with open("test.txt", "rb") as original:
        originalData = original.read()

    with open(outputPath, "rb") as received:
        receivedData = received.read()

    print(
        "Files match:",
        originalData == receivedData
    )