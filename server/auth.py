import bcrypt
from .database import Database
from client.keys import KeyManager

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

    def register(self,username,password,publicKey):
        if self.userExists(username):
            return False
        
        passHash=self.hashPass(password)

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
                publicKey
            )
        )
        return True

    def login(self,username,password):
        
        user=self.db.fetchOne("SELECT password_hash FROM users WHERE username=?",
        (username,))

        if user is None:
            return False
        
        storedHash=user[0]

        return self.verifyPass(password,storedHash)

    def logout(self):
        self.currentUser=None