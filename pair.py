class PairManager:

    def __init__(self,db):
        self.db=db

    def getUserID(self,username):

        user=self.db.fetchOne(
            "SELECT id FROM users WHERE username=?",
            (username,)
        )

        if user is None:
            return None

        return user[0]

    def requestPair(self,u1,u2):

        if u1==u2:
            return False

        user1ID=self.getUserID(u1)
        user2ID=self.getUserID(u2)

        if user1ID is None or user2ID is None:
            return False

        # Check whether either user is already paired
        exists=self.db.fetchOne(
            """
            SELECT id FROM pairs
            WHERE (user1=? OR user2=?)
            AND status IN ('pending', 'accepted')
            """,
            (user1ID, user1ID)
        )

        if exists is not None:
            return False

        exists=self.db.fetchOne(
            """
            SELECT id FROM pairs
            WHERE (user1=? OR user2=?)
            AND status IN ('pending', 'accepted')
            """,
            (user2ID, user2ID)
        )

        if exists is not None:
            return False

        self.db.execute(
            """
            INSERT INTO pairs(user1,user2,status)
            VALUES(?,?,?)
            """,
            (user1ID,user2ID,"pending")
        )

        return True

    def respondToPair(self,u1,u2,response):

        user1ID=self.getUserID(u1)
        user2ID=self.getUserID(u2)

        if user1ID is None or user2ID is None:
            return False

        pair=self.db.fetchOne(
            """
            SELECT id FROM pairs
            WHERE user1=?
            AND user2=?
            AND status='pending'
            """,
            (user2ID,user1ID)
        )

        if pair is None:
            return False

        pairID=pair[0]

        response=response.lower()

        if response=="accept":

            self.db.execute(
                """
                UPDATE pairs
                SET status='accepted'
                WHERE id=?
                """,
                (pairID,)
            )

            return True

        elif response=="reject":

            self.db.execute(
                """
                DELETE FROM pairs
                WHERE id=?
                """,
                (pairID,)
            )

            return True

        return False

    def isPaired(self,u1,u2):

        user1ID=self.getUserID(u1)
        user2ID=self.getUserID(u2)

        if user1ID is None or user2ID is None:
            return False

        pair=self.db.fetchOne(
            """
            SELECT id FROM pairs
            WHERE
                (
                    (user1=? AND user2=?)
                    OR
                    (user1=? AND user2=?)
                )
                AND status='accepted'
            """,
            (
                user1ID,
                user2ID,
                user2ID,
                user1ID
            )
        )

        return pair is not None

    def getPartner(self, username):

        user = self.db.fetchOne(
            "SELECT id FROM users WHERE username=?",
            (username,)
        )

        if user is None:
            return None

        userID = user[0]

        partner = self.db.fetchOne(
            """
            SELECT u.username
            FROM pairs p
            JOIN users u
                ON u.id =
                    CASE
                        WHEN p.user1 = ? THEN p.user2
                        ELSE p.user1
                    END
            WHERE (p.user1=? OR p.user2=?)
            AND p.status='accepted'
            """,
            (userID, userID, userID)
        )

        if partner is None:
            return None

        return partner[0]