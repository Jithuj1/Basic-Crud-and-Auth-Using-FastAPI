from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi import APIRouter
import secrets
import schemas
import student
from database import SessionLocal
from starlette.requests import Request
from fastapi.responses import Response
from starlette.applications import Starlette
from starlette.middleware.sessions import SessionMiddleware
from fastapi.responses import JSONResponse


router = APIRouter()

app = Starlette()

random_secret_key = secrets.token_hex(32)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#  for login 

@router.post("/login/")
async def login(data:schemas.StudentCreate, request: Request, db: Session = Depends(get_db)):
    user = student.check_user(db=db, data=data)
    if user:
        response = JSONResponse({"message": "Logged in successfully"})
        response.set_cookie(key="username", value=data.username, max_age=1800) 
        return response   
    else: raise HTTPException(status_code=401, detail="Invalid username or password")


@router.get("/home")
def dashboard(request: Request):
    if request.cookies.get("username"):
        username = request.cookies.get("username")
        return {"message": f"Welcome, {username}!"}
    else:
        raise HTTPException(status_code=401, detail="Not authenticated")
    

@router.post("/logout")
def logout(request: Request):
    if 'username' in request.cookies:
        response = JSONResponse({"message": "Logged in successfully"})
        response.delete_cookie("username") 
        return response   
