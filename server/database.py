import sqlite3
import os

class Database:

    def __init__(self):
        self.dbPath="data/messenger.db"
        os.makedirs("data",exist_ok=True)
        self.createTables()

    def connect(self):
        return sqlite3.connect(self.dbPath)

    def createTables(self):
        connection=self.connect()
        cursor=connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            public_key TEXT
            )
            """)
        cursor.execute("""
                CREATE TABLE IF NOT EXISTS pairs(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user1 TEXT NOT NULL,
                user2 TEXT NOT NULL,
                status TEXT NOT NULL
                )
                """)
        cursor.execute("""
                CREATE TABLE IF NOT EXISTS messages(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sender TEXT NOT NULL,
                receiver TEXT NOT NULL,
                message TEXT NOT NULL,
                timestamp TEXT NOT NULL
                )
                """)

        cursor.execute("""
                CREATE TABLE IF NOT EXISTS files(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sender TEXT NOT NULL,
                    receiver TEXT NOT NULL,
                    filename TEXT NOT NULL,
                    data TEXT NOT NULL,
                    timestamp TEXT NOT NULL
                )
                """)
        connection.commit()
        connection.close()

    def execute(self,query,values=()):
        connection=self.connect()
        cursor=connection.cursor()

        cursor.execute(query,values)

        connection.commit()
        connection.close()

    def fetchOne(self,query,values=()):
        connection=self.connect()
        cursor=connection.cursor()
        
        cursor.execute(query,values)
        result=cursor.fetchone()
        connection.close()

        return result

    def fetchAll(self,query,values=()):
        connection=self.connect()
        cursor=connection.cursor()
            
        cursor.execute(query,values)
        result=cursor.fetchall()
        connection.close()
    
        return result