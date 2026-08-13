# Paired Secure Messenger

A Python-based CLI secure messaging application that allows paired users to exchange **encrypted messages and files** using modern cryptographic techniques.

## Features

* User Registration & Login
* Password Hashing with bcrypt
* One-to-One User Pairing
* X25519 Key Exchange
* HKDF Key Derivation
* AES-GCM Message Encryption
* Encrypted File Transfer
* Persistent Private Key Storage
* SQLite Database
* CLI Interface

## Security

* Passwords are hashed using **bcrypt**
* X25519 is used for secure key exchange
* HKDF is used to derive encryption keys
* AES-GCM provides authenticated encryption
* Private keys are stored locally and are not stored in the database

## Project Structure

```text
.
├── auth.py
├── crypto.py
├── database.py
├── filemanager.py
├── keys.py
├── message.py
├── pair.py
├── main.py
├── requirements.txt
├── database/
├── keys/
└── files/
```

## Technologies

* Python
* SQLite
* Cryptography
* bcrypt
* X25519
* HKDF
* AES-GCM
* Object-Oriented Programming

## Current Functionality

* Register and authenticate users
* Send and accept pairing requests
* Establish pair-specific encryption keys
* Send and receive encrypted messages
* Send and receive encrypted files
* Store encrypted data in SQLite
* Run the application through a CLI

## How It Works

```text
User A
   ↓
X25519 Key Exchange
   ↓
HKDF
   ↓
AES-GCM
   ↓
Encrypted Message/File
   ↓
SQLite
   ↓
Decrypt
   ↓
User B
```

## Statistics / Security Components

* Password hashing using bcrypt
* X25519 key exchange
* HKDF-SHA256 key derivation
* AES-256-GCM encryption
* Persistent X25519 private keys
* Encrypted message and file storage

## Future Improvements

* FastAPI backend
* Real-time messaging using WebSockets
* PostgreSQL database
* Separate network-based clients
* React frontend
* Online/offline status
* Improved private key protection
* End-to-end network communication

## Requirements

* Python 3
* bcrypt
* cryptography

## Run

```bash
python main.py
```

## Author

Yash Thakur
