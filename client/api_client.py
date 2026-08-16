import requests

class APIClient:
    def __init__(self,baseURL="http://127.0.0.1:8000"):
        self.baseURL=baseURL
        self.token=None

    def register(self,username,password,publicKey):
        response=requests.post(
            f"{self.baseURL}/register",
            json={
                "username":username,
                "password":password,
                "publicKey":publicKey
            }
        )
        return response.json()
    def login(self, username,password):
        response=requests.post(
            f"{self.baseURL}/login",
            json={
                "username":username,"password":password
            }
        )
        result=response.json()
        if result.get("success"):
            self.token=result["token"]

        return result
    def getMe(self):
        response=requests.get(
            f"{self.baseURL}/me",
            headers={
                "Authorisation":f"Bearer {self.token}"
            }
        )
        return response.json()

    def requestPair(self,username):
        response=requests.post(
            f"{self.baseURL}/pair/request",
            json={
                "username":username
            },
            headers={
                "Authorisation":f"Bearer {self.token}"
            }
        )
        return response.json()

    def respondPair(self,username,response):
        result=requests.post(
            f"{self.baseURL}/pair/respond",
            json={
                "username":username,
                "response":response
            },
            headers={
                "Authorisation":f"Bearer {self.token}"
            }
        )
        return result.json()

    def getPartner(self):
        response=requests.get(f"{self.baseURL}/pair/partner",
                              headers={
                                  "Authorisation":f"Bearer {self.token}"
                              })
        return response.json()
    def getPublicKey(self,username):
        response=requests.get(f"{self.baseURL}/users/{username}/publicKey",
                              headers={"Authorisation":f"Bearer {self.token}"
                                       })
        return response.json()
    def sendMessage(self,receiver,encryptedMessage):
        response=requests.post(
            f"{self.baseURL}/messages",
            json={
                "receiver":receiver,
                "message":encryptedMessage
            },
            headers={
                "Authorisation":f"Bearer {self.token}"
            }
        )
        return response.json()
    def getMessages(self,partner):
        response=requests.get(
            f"{self.baseURL}/messages/{partner}",
            headers={
                "Authorisation":f"Bearer {self.token}"
            }
        )
        return response.json()