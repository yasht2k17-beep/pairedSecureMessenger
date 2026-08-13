import bcrypt
from database import Database
from keys import KeyManager

class Auth:
    def __init__(self,db):
        self.db=db
        self.currentUser=None

    def hashPass(self,password):
        salt=bcrypt.gensalt()

        passHash=bcrypt.hashpw(password.encode(),salt)

        return passHash.decode()

    def verifyPass(self,password,passHash):
        return bcrypt.checkpw(password.encode(),passHash.encode())

    def userExists(self,username):
        user=self.db.fetchOne("SELECT * FROM users WHERE username=?",(username,))
        return user is not None

    def register(self,username,password):
        if self.userExists(username):
            return False
        
        passHash=self.hashPass(password)

        keyManager = KeyManager(username)

        privateKey = keyManager.getPrivateKey()
        publicKey = keyManager.getPublicKey(privateKey)

        publicKeyBytes = publicKey.public_bytes_raw()

        self.db.execute(
            """
            INSERT INTO users(
                username,
                password_hash,
                public_key
            )
            VALUES(?, ?, ?)
            """,
            (
                username,
                passHash,
                publicKeyBytes.hex()
            )
        )

        self.currentUser=username
        return True

    def login(self,username,password):
        if not self.userExists(username):
            return False
        user=self.db.fetchOne("SELECT password_hash FROM users WHERE username=?",
        (username,))

        storedHash=user[0]

        if self.verifyPass(password,storedHash):
            self.currentUser=username
            return True
        return False

    def logout(self):
        self.currentUser=None