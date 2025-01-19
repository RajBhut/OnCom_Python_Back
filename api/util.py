# from fastapi import  HTTPException, Request, Response

# from jose import JWTError, jwt
# from passlib.context import CryptContext

# from datetime import datetime, timedelta
# from typing import Optional
# import os
# from api.db import prisma


# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# SECRET_KEY = os.getenv("JWT_SECRET", "your_secret_key")
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_DAYS = 14  
# uviCOOKIE_MAX_AGE = 60 * 60 * 24 * ACCESS_TOKEN_EXPIRE_DAYS 
# def get_password_hash(password: str) -> str:
#     return pwd_context.hash(password)


# def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.utcnow() + expires_delta
#     else:
#         expire = datetime.utcnow() + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt


# async def get_current_user(request: Request):
#     token = request.cookies.get("jwt")
    
#     if not token:
#         raise HTTPException(status_code=401, detail="Not authenticated")
    
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         user_id = payload.get("sub")
#         if user_id is None:
#             raise HTTPException(status_code=401, detail="Invalid token")
        
        
#         try:
#             db_user_id = int(user_id)
#         except ValueError:
#             raise HTTPException(status_code=401, detail="Invalid user ID format")
            
#         user = await prisma.user.find_unique(where={"id": db_user_id})
#         if user is None:
#             raise HTTPException(status_code=401, detail="User not found")
#         return user
#     except JWTError as e:
#         print(f"JWTError: {str(e)}")
#         raise HTTPException(status_code=401, detail="Invalid token")

from fastapi import HTTPException, Request
from jose import JWTError, jwt
from passlib.context import CryptContext

from datetime import datetime, timedelta
from typing import Optional
from .db import supabase
import os



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = os.getenv("JWT_SECRET", "your_secret_key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 14
COOKIE_MAX_AGE = 60 * 60 * 24 * ACCESS_TOKEN_EXPIRE_DAYS


def get_password_hash(password: str) -> str:
    """Hash a password using bcrypt."""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT token with an optional expiration."""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(request: Request):
    """Retrieve the currently authenticated user."""
    token = request.cookies.get("jwt")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")

        # Fetch user from Supabase
        response = supabase.table("User").select("*").eq("id", user_id).execute()
        if  not response.data:
            raise HTTPException(status_code=401, detail="User not found")

        return response.data[0]  # Return user data
    except JWTError as e:
        print(f"JWTError: {str(e)}")
        raise HTTPException(status_code=401, detail="Invalid token")
