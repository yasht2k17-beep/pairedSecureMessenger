from fastapi import FastAPI,Header,HTTPException
from pydantic import BaseModel
from .database import Database
from .auth import Auth
from .pair import PairManager
from .message import Message
from datetime import datetime,timedelta,timezone
from jose import jwt

SECRET_KEY="1234"
ALGORITHM="HS256"

app = FastAPI()
db=Database()
auth =Auth(db)
pair=PairManager(db)
messages=Message(db,pair)

class RegisterRequest(BaseModel):
    username:str
    password:str
    publicKey:str

@app.get("/")
def home():
    return{
        "message":"Paired Secure Messenger Server"
    }
@app.post("/register")
def register(request:RegisterRequest):
    success=auth.register(request.username,request.password,request.publicKey)

    if success:
        return {
            "success":True,
            "message":"Registration Successful"
        }
    return {
        "success":False,
        "message":"Username exists"
    }

class LoginRequest(BaseModel):
    username:str
    password:str

@app.post("/login")
def login(request:LoginRequest):
    success=auth.login(
        request.username,request.password
    )

    if not success:
        return {
            "success":False,
            "message":"Invalid username or password"
        }
    token=createToken(request.username)
    return{
        "success":True,
        "message":"Login Successful",
        "token":token
        }

def createToken(username):
    payload={
        "sub":username,
        "exp":datetime.now(timezone.utc)+timedelta(hours=1)
    }
    return jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)

def getCurrentUser(authorisation):
    if not authorisation:
        raise HTTPException(
            status_code=401,detail="Missing Token"
        )
    try:
        token=authorisation.split(" ")[1]
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])

        return payload["sub"]
    
    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invaid or expired Token"
        )
@app.get("/me")
def getMe(authorisation:str=Header(None)):
    username=getCurrentUser(authorisation)
    return {
        "username":username
    }

class PairRequest(BaseModel):
    username:str
class PairResponse(BaseModel):
    username:str
    response:str

@app.post("/pair/request")
def requestPair(request:PairRequest,authorisation:str=Header(None)):
    sender=getCurrentUser(authorisation)
    success=pair.requestPair(sender,request.username)

    if success:
        return{
            "success":True,
            "message":"Pair Request Sent"
        }
    return{
        "success":False,
        "message":"Couldn't Send Pair Request"
    }

@app.post("/pair/respond")
def respondPair(request:PairResponse,authorisation:str=Header(None)):
    receiver=getCurrentUser(authorisation)
    success=pair.respondToPair(receiver,request.username,request.response)

    if success:
        return{
                    "success":True,
                    "message":f"Pair Request {request.response}ed"
                }
    return{
            "success":False,
            "message":"No Pending Requests"
        }

@app.get("/pair/partner")
def getPartner(authorisation:str=Header(None)):
    username=getCurrentUser(authorisation)
    partnerUsername=pair.getPartner(username)

    if partnerUsername is None:
        return{
            "success":False,
            "partner":None
        }
    return{
        "success":True,
        "partner":partnerUsername
    }

class SendMessageRequest(BaseModel):
    receiver:str
    message:str

@app.post("/messages")
def sendMessage(request:SendMessageRequest,authorisation:str=Header(None)):
    sender=getCurrentUser(authorisation)

    success=messages.send(sender,request.receiver,request.message)

    if success:
        return{
            "success":True,
            "message":"Message Sent"
        }
    return {
        "success":False,
        "message":"Message not Sent"
    }

@app.get("/messages/{partner}")
def getMessages(partner:str,authorisation:str=Header(None)):
    username=getCurrentUser(authorisation)

    result=messages.getMessages(username,partner)

    if not result:
        return{
            "success":False,
            "messages":[]
        }
    return {
        "success":True,
        "messages":result
    }
@app.get("/users/{username}/publicKey")
def getPublicKey(username:str,authorisation:str=Header(None)):
    getCurrentUser(authorisation)

    user=db.fetchOne(
        """
        SELECT public_key
        FROM users
        WHERE username=?
        """,
        (username,)
    )

    if user is None:
        return{
            "success":False,
            "message":"User not Found"
        }
    return{
        "success":True,
        "publicKey":user[0]
    }