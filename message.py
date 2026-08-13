import base64

from crypto import Crypto
from keys import KeyManager

from cryptography.hazmat.primitives.asymmetric.x25519 import (
    X25519PublicKey)


class Message:
    def __init__(self,db,pairManager):

        self.db=db
        self.pairManager=pairManager

    def getPublicKey(self,username):

        user=self.db.fetchOne(
            "SELECT public_key FROM users WHERE username=?",
            (username,))

        if user is None:
            return None

        return bytes.fromhex(user[0])

    def getSharedKey(self,username,partner):

        keyManager=KeyManager(username)

        privateKey=keyManager.getPrivateKey()

        publicKeyBytes=self.getPublicKey(partner)

        if publicKeyBytes is None:
            return None

        publicKey=X25519PublicKey.from_public_bytes(
            publicKeyBytes)

        sharedSecret=Crypto.genSharedSecret(privateKey,publicKey)

        return Crypto.deriveKey(sharedSecret)

    def send(self,sender,receiver,msg):

        if not self.pairManager.isPaired(sender,receiver):
            return False

        key=self.getSharedKey(sender,receiver)

        if key is None:
            return False

        crypto=Crypto(key)

        encrypted=crypto.encrypt(msg)

        encrypted=base64.b64encode( encrypted).decode()

        self.db.execute(
            """
            INSERT INTO messages(
                sender,
                receiver,
                message,
                timestamp
            )
            VALUES(?, ?, ?, datetime('now'))
            """,
            (sender,receiver,encrypted)
        )

        return True

    def getMessages(self,u1,u2):

        if not self.pairManager.isPaired(u1,u2):
            return []

        key = self.getSharedKey(u1,u2)

        if key is None:
            return []
        
        crypto=Crypto(key)

        messages=self.db.fetchAll(
            """
            SELECT sender, receiver, message, timestamp
            FROM messages
            WHERE (sender=? AND receiver=?)
               OR (sender=? AND receiver=?)
            ORDER BY id ASC
            """,
            (u1,u2,u2,u1)
        )

        result=[]

        for sender,receiver,encrypted,timestamp in messages:

            encrypted=base64.b64decode(encrypted)

            msg=crypto.decrypt(encrypted)

            result.append({
                "sender": sender,
                "receiver": receiver,
                "message": msg,
                "timestamp": timestamp
            })
            
        return result