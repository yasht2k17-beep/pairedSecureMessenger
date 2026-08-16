import base64

class Message:
    def __init__(self,db,pairManager):

        self.db=db
        self.pairManager=pairManager


    def send(self,sender,receiver,encryptedMessage):

        if not self.pairManager.isPaired(sender,receiver):
            return False


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
            (sender,receiver,encryptedMessage)
        )

        return True

    def getMessages(self,u1,u2):

        if not self.pairManager.isPaired(u1,u2):
            return []

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
            result.append({
                "sender": sender,
                "receiver": receiver,
                "message": encrypted,
                "timestamp": timestamp
            })
            
        return result