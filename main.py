from fastapi import FastAPI, Depends, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from jose import JWTError, jwt
from passlib.context import CryptContext
from db import prisma
from datetime import datetime, timedelta
from typing import Optional, List
import os
from pydantic import BaseModel, EmailStr
from util import create_access_token,get_current_user,get_password_hash
from routers import problem_route
app = FastAPI()

app.include_router(problem_route.router ,prefix="/problem")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600,
)



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = os.getenv("JWT_SECRET", "your_secret_key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 80


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

@app.on_event("startup")
async def startup():
    await prisma.connect()

@app.on_event("shutdown")
async def shutdown():
    await prisma.disconnect()

@app.get("/test/{name}")
def test(name: str):
    return {"message": f"Hello, {name}"}

@app.post("/users/register")
async def register_user(user: UserRegister, response: Response):
    hashed_password = get_password_hash(user.password)
    try:
        new_user = await prisma.user.create(
            data={
                "email": user.email,
                "password": hashed_password,
                "name": user.name,
            }
        )
        
        user_data = {
            "id": new_user.id,
            "email": new_user.email,
            "name": new_user.name
        }
        
        access_token = create_access_token(
            data={"sub": str(new_user.id)},
            expires_delta=timedelta(days=ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        response.set_cookie(key="jwt", value=access_token, httponly=True, secure=True)
        
        return {
            "message": "User registered successfully",
            "user": user_data
        }
    except Exception as e:
        if "Unique constraint" in str(e):
            raise HTTPException(
                status_code=400,
                detail="Email already exists"
            )
        print(f"Registration error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Error registering user"
        )
    

# @app.post("/problem")
# async def create_question(problem: Problem, current_user=Depends(get_current_user)):
#     new_problem = await prisma.problem.create(
#         data={
#             "title": problem.title,
#             "description": problem.description,
#             "difficulty": problem.difficulty,
#             "tags": problem.tags,
#             "creatorId": current_user.id
#         }
#     )
#     return {"message": "Problem created successfully", "problem": new_problem}

@app.post("/users/login")
async def login_user(user: UserLogin, response: Response):
    user_data = await prisma.user.find_first(
        where={
            "email": user.email
        }
    )
    if not user_data:
        raise HTTPException(
            status_code=400,
            detail="Invalid email or password"
        )
    if not pwd_context.verify(user.password, user_data.password):
        raise HTTPException(
            status_code=400,
            detail="Invalid email or password"
        )
    access_token = create_access_token(
        data={"sub": str(user_data.id)},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    response.set_cookie(key="jwt", value=access_token, httponly=True, secure=True)
    return {"message": "Logged in successfully","user": user_data}

@app.get("/users/profile")
async def get_user_profile(current_user=Depends(get_current_user)):
    return current_user

@app.post("/users/logout")
async def logout_user(response: Response):
    response.delete_cookie("jwt")
    return {"message": "Logged out successfully"}


