# server.py
from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
import rhino_health as rh
import uuid

app = FastAPI()
sessions = {}

class LoginRequest(BaseModel):
    username: str
    password: str

@app.post("/login")
def login(req: LoginRequest):
    try:
        session = rh.login(username=req.username, password=req.password, rhino_api_url=rh.lib.constants.ApiEnvironment.DEMO_DEV_URL)
        session_id = str(uuid.uuid4())
        sessions[session_id] = session
        return {"session_id": session_id}
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

@app.get("/projects")
def get_projects(session_id: str = Header(...)):
    session = sessions.get(session_id)
    if not session:
        raise HTTPException(status_code=401, detail="Invalid or expired session_id")
    try:
        projects = session.project.get_projects()
        return {"projects": [p.dict() for p in projects]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

