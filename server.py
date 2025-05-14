# server.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import rhino_health as rh

app = FastAPI()

class LoginRequest(BaseModel):
    username: str
    password: str

@app.post("/login")
def login(req: LoginRequest):
    try:
        session = rh.login(username=req.username, password=req.password)
        return {"current_user": session.current_user}
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

