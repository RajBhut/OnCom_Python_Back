from typing import Any, Dict, List, Optional
from db import prisma
from pydantic import BaseModel, EmailStr
from util import create_access_token,get_current_user,get_password_hash

from fastapi import APIRouter, Depends, HTTPException, Request
import base64
import urllib.parse

def decode_js_data(encoded_data: str):
  
    base64_decoded = base64.b64decode(encoded_data).decode('utf-8')
   
    url_decoded = urllib.parse.unquote(base64_decoded)
    return url_decoded


router = APIRouter()

class Problem(BaseModel):
    title: str
    description: str
    difficulty: str
    tags: List[str]

class Code(BaseModel):
    
    function:str
    language :str
    testcases:str
    checker:str
    problemId:int
    userId:int
    creatorId:int

class Notes_data(BaseModel):
    edge:str
    node:str
    

@router.post("/")
async def create_question(problem: Problem, current_user=Depends(get_current_user)):
    new_problem = await prisma.problem.create(
        data={
            "title": problem.title,
            "description": problem.description,
            "difficulty": problem.difficulty,
            "tags": problem.tags,
            "creatorId": current_user.id
        }
    )
    return {"message": "Problem created successfully", "problem": new_problem}

@router.get("/")
async def get_problems():
    problems = await prisma.problem.find_many()
    return problems

@router.get("/self/{id}")
async def get_problems(id:int):
    Problems = await prisma.problem.find_many(
        where= {
            "creatorId": id}
        
    )
    return Problems


@router.get("/one/{id}")
async def get_single(id:int):
    data = {}
    try:
       
        data = await prisma.problem_code.find_many(where={"problemId":id})
        
        if data ==None:
            return {}
        else:
            return data
        
        

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500,detail="error in fetching problem")
    
    
@router.post("/update/{id}")
async def add_notes(id:int,Data:Notes_data):
    
 
    try:
        data = await prisma.problem.update(
            where={"id":id},
            data={
                "edgedata":Data.edge,
                "nodedata":Data.node
            }
        )
        return data
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500,detail="error in updating problem")
    


@router.get("/update/{id}")
async def get_update(id:int):
    try:
        data = await prisma.problem.find_first(where={
            "id":id
        },
        )
        
        return data
        
        
    except Exception as e:
        print(e)
        raise HTTPException(status_code=403 ,detail="Error in fatching notes")

  
@router.get("/data/{id}")
async def get_single(id:int):
    
    data = {}
    try:
       
        data = await prisma.problem.find_many(where={"id":id})
        
        if data ==None:
            
            
            return {}
        else:
            
            return data
        
        

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500,detail="error in fetching problem")
    




@router.post("/add")
async def add_code(data: Code, current_user=Depends(get_current_user)):
    if data.creatorId != data.userId:
        raise HTTPException(status_code=401, detail="not authorised")
    try:
        code = await prisma.problem_code.upsert(
        where={"problemId_language": {"problemId": int(data.problemId), "language": decode_js_data(data.language).upper()}},
        data={
            "update": {
                "function": data.function,
                "testcases": data.testcases,
                "checker": data.checker,
                "userId": data.userId,
            },
            "create": {
                "function": data.function,
                "language": decode_js_data(data.language).upper(),
                "testcases": data.testcases,
                "checker": data.checker,
                "problemId": int(data.problemId),
                "userId": data.userId,
            }
        }
    )
        return {"message": "Code added successfully", "code": code}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="error in fetching problem")
