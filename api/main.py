

from fastapi import FastAPI, Depends, HTTPException,  Response
from fastapi.middleware.cors import CORSMiddleware
from passlib.context import CryptContext
from datetime import  timedelta
from typing import  List
import os
from pydantic import BaseModel, EmailStr

from api.util import create_access_token, get_current_user, get_password_hash
from api.routers import problem_route as pr

from .db import supabase 
app = FastAPI()

app.include_router(pr.router, prefix="/problem")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173","https://oncomp.rajb.codes","https://on-comp-frontend.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600,
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = os.getenv("JWT_SECRET", "your_secret_key")
ALGORITHM = "HS256"
COOKIE_MAX_AGE = 7 * 24 * 60 * 60 




class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserRegister(BaseModel):
    email: EmailStr
    password: str
    name: str


class Problem(BaseModel):
    title: str
    description: str
    difficulty: str
    tags: List[str]


@app.get("/")
def test():
    return {"message": f"Hello World"}



# @app.post("/users/register")
# async def register_user(user: UserRegister, response: Response):
#     hashed_password = get_password_hash(user.password)
#     try:
#         result = supabase.table("User").select("*").eq("email", user.email).execute()
     
#         if result.data:
#             raise HTTPException(status_code=400, detail="Email already registered")
        
        
#         result = supabase.table("User").insert({
#             "email": user.email,
#             "password": hashed_password,
#             "name": user.name,
#         }).execute()
       
#         if not result.data:
#             raise HTTPException(status_code=500, detail="Error creating user")
        
#         db_user = result.data[0]
        
#         access_token_expires = timedelta(days=7)
#         access_token = create_access_token(
#             data={"sub": str(db_user["id"])}, expires_delta=access_token_expires
#         )
#         response.set_cookie(key="jwt", value=access_token, httponly=True, secure=True)
        
#         return {"message": "User registered successfully", "user": {"id": db_user["id"], "email": db_user["email"], "name": db_user["name"]}}
#     except Exception as e:
#         print(f"Error: {e}")
#         raise HTTPException(status_code=500, detail="Error in registering user")

@app.post("/users/register")
async def register_user(user: UserRegister, response: Response):
    hashed_password = get_password_hash(user.password)
    try:
        # Check if the user already exists
        result = supabase.table("User").select("*").eq("email", user.email).execute()
        if result.data:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Create the user in the database
        result = supabase.table("User").insert({
            "email": user.email,
            "password": hashed_password,
            "name": user.name,
        }).execute()
        
        if not result.data:
            raise HTTPException(status_code=500, detail="Error creating user")
        
        db_user = result.data[0]
        
        # Create access token
        access_token_expires = timedelta(seconds=COOKIE_MAX_AGE)
        access_token = create_access_token(
            data={"sub": str(db_user["id"])}, expires_delta=access_token_expires
        )
        response.set_cookie(
            key="jwt",
            value=access_token,
            httponly=True,
            secure=True,
            max_age=COOKIE_MAX_AGE,
            expires=COOKIE_MAX_AGE
        )
        
        return {"message": "User registered successfully", "user": {"id": db_user["id"], "email": db_user["email"], "name": db_user["name"]}}
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Error in registering user")


# @app.post("/users/login")
# async def login(user: UserLogin, response: Response):
#     result = supabase.table("User").select("*").eq("email", user.email).execute()
#     db_user = result.data[0] if result.data else None
    
#     if not db_user: 
#         raise HTTPException(status_code=400, detail="Invalid email or password")
    
#     if not pwd_context.verify(user.password, db_user["password"]):
#         raise HTTPException(status_code=400, detail="Invalid email or password")
    
#     access_token_expires = timedelta(days=COOKIE_MAX_AGE)
#     access_token = create_access_token(
#         data={"sub": str(db_user["id"])}, expires_delta=access_token_expires
#     )
#     response.set_cookie(key="jwt", value=access_token, httponly=True, secure=True)
#     print("dbuser"+db_user)
#     return {"message": "Logged in successfully", "user": {"id": db_user["id"], "email": db_user["email"], "name": db_user["name"]}}

@app.post("/users/login")
async def login(user: UserLogin, response: Response):
    try:
            
        result = supabase.table("User").select("*").eq("email", user.email).execute()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="Invalid email or password")
        
    db_user = result.data[0] if result.data else None
    
    if not db_user: 
        raise HTTPException(status_code=400, detail="Invalid email or password")
    
    if not pwd_context.verify(user.password, db_user["password"]):
        raise HTTPException(status_code=400, detail="Invalid email or password")
    
    access_token_expires = timedelta(seconds=COOKIE_MAX_AGE)
    access_token = create_access_token(
        data={"sub": str(db_user["id"])}, expires_delta=access_token_expires
    )
    response.set_cookie(
        key="jwt",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="None",
        max_age=COOKIE_MAX_AGE,
        expires=COOKIE_MAX_AGE
    )
    
    return {"message": "Logged in successfully", "user": {"id": db_user["id"], "email": db_user["email"], "name": db_user["name"]}}


@app.get("/users/profile")
async def get_user_profile(current_user=Depends(get_current_user)):
    return current_user


@app.post("/users/logout")
async def logout_user(response: Response):
    response.delete_cookie("jwt")
    return {"message": "Logged out successfully"}
