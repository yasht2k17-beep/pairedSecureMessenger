import os
import base64
from client.crypto import Crypto
from client.keys import KeyManager
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PublicKey

class FileManager:
    def __init__(self,db,pairManager):
        self.db=db
        self.pairManager=pairManager
        self.fileDir="files"
        os.makedirs(self.fileDir,exist_ok=True)

    def getPublicKey(self,username):
        user=self.db.fetchOne(
            "SELECT public_key FROM users WHERE username=?",
            (username,)
        )

        if user is None:
            return None
        return bytes.fromhex(user[0])

    def getSharedKey(self,username,partner):
        keyManager=KeyManager(username)
        privateKey=keyManager.getPrivateKey()
        publicKeyBytes=self.getPublicKey(partner)

        if publicKeyBytes is None:
            return None

        publicKey=X25519PublicKey.from_public_bytes(publicKeyBytes)
        sharedSecret=Crypto.genSharedSecret(privateKey,publicKey)

        return Crypto.deriveKey(sharedSecret)

    def sendFile(self,sender,receiver,filePath):

        if not self.pairManager.isPaired(sender,receiver):
            return False

        if not os.path.exists(filePath):
            return False

        key=self.getSharedKey(sender,receiver)

        if key is None:
            return False

        crypto=Crypto(key)

        with open(filePath,"rb") as file:
            data=file.read()

        encrypted=crypto.encryptBytes(data)
        encrypted=base64.b64encode(encrypted).decode()

        fileName=os.path.basename(filePath)

        self.db.execute(
            """
            INSERT INTO files(
                sender,
                receiver,
                filename,
                data,
                timestamp
            )
            VALUES(?, ?, ?, ?, datetime('now'))
            """,
            (
                sender,
                receiver,
                fileName,
                encrypted
            )
        )

        return True

    def getFiles(self,u1,u2):
        if not self.pairManager.isPaired(u1,u2):
            return []

        files=self.db.fetchAll(
            """
            SELECT id, sender, receiver, filename, timestamp
            FROM files
            WHERE (sender=? AND receiver=?)
            OR (sender=? AND receiver=?)
            ORDER BY id ASC
            """,
            (u1,u2,u2,u1)
        )
        return files

    def downloadFile(self,fileID,username,partner):
        if not self.pairManager.isPaired(username,partner):
            return False

        file=self.db.fetchOne(
            """
            SELECT filename, data
            FROM files
            WHERE id=?
            """,
            (fileID,)
        )
        if file is None:
            return False

        filename=file[0]
        encrypted=file[1]

        key=self.getSharedKey(username,partner)
        if key is None:
            return False

        crypto=Crypto(key)
        encrypted=base64.b64decode(encrypted)
        data=crypto.decryptBytes(encrypted)

        outputPath=os.path.join(self.fileDir,"received_"+filename)

        with open(outputPath,"wb") as output:
            output.write(data)

        return outputPath
        