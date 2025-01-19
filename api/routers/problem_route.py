
from typing import Any, Dict, List
from api.util import create_access_token,get_current_user,get_password_hash
from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException
import base64
import os
import urllib.parse

from ..db import supabase 

def decode_js_data(encoded_data: str):
    base64_decoded = base64.b64decode(encoded_data).decode("utf-8")
    url_decoded = urllib.parse.unquote(base64_decoded)
    return url_decoded

router = APIRouter()

class Problem(BaseModel):
    title: str
    description: str
    difficulty: str
    tags: List[str]

class Code(BaseModel):
    function: str
    language: str
    testcases: str
    checker: str
    problemId: int
    userId: int
    creatorId: int

class NotesData(BaseModel):
    edge: str
    node: str

@router.post("/")
async def create_question(problem: Problem, current_user=Depends(get_current_user)):
    try:
        
        new_problem = supabase.table("Problem").insert({
            "title": problem.title,
            "description": problem.description,
            "difficulty": problem.difficulty,
            "tags": problem.tags,
            "creatorid": current_user["id"]
        }).execute()

        if not new_problem.data:
            raise HTTPException(status_code=400, detail="Failed to create problem")

        return {"message": "Problem created successfully", "problem": new_problem.data[0]}
    except Exception as e:
        print(f"Error creating problem: {e}")
        raise HTTPException(status_code=500, detail="Error creating problem")

@router.get("/")
async def get_problems():
    try:
        problems = supabase.table("Problem").select("*").execute()
        
        return problems.data
    except Exception as e:
        print(f"Error fetching problems: {e}")
        raise HTTPException(status_code=500, detail="Error fetching problems")

@router.get("/self/{id}")
async def get_problems_by_creator(id: int):
    try:
        problems = supabase.table("Problem").select("*").eq("creatorid", id).execute()
        return problems.data
    except Exception as e:
        print(f"Error fetching problems by creator: {e}")
        raise HTTPException(status_code=500, detail="Error fetching problems by creator")

@router.get("/one/{id}")
async def get_problem_codes(id: int):
    try:
        codes = supabase.table("Problem_code").select("*").eq("problemid", id).execute()
        
        return codes.data or []
    except Exception as e:
        print(f"Error fetching problem codes: {e}")
        raise HTTPException(status_code=500, detail="Error fetching problem codes")

@router.post("/update/{id}")
async def update_problem_notes(id: int, data: NotesData):
    try:
        
        
        updated_problem = supabase.table("Problem").update({
            "edgedata": data.edge,
            "nodedata": data.node
        }).eq("id", id).execute()

        if not updated_problem.data:
            raise HTTPException(status_code=400, detail="Failed to update problem")

        return updated_problem.data[0]
    except Exception as e:
        print(f"Error updating problem notes: {e}")
        raise HTTPException(status_code=500, detail="Error updating problem notes")

@router.get("/update/{id}")
async def get_problem_by_id(id: int):
    try:
        problem = supabase.table("Problem").select("*").eq("id", id).execute()
     
        return problem.data[0] if problem.data else {}
    except Exception as e:
        print(f"Error fetching problem by ID: {e}")
        raise HTTPException(status_code=500, detail="Error fetching problem by ID")

@router.post("/add")
async def add_code(data: Code, current_user=Depends(get_current_user)):
    if data.creatorId != data.userId:
        raise HTTPException(status_code=401, detail="Not authorized")

    try:
        code = supabase.table("Problem_code").upsert({
            "problemid": data.problemId,
            "language": decode_js_data(data.language).upper(),
            "function": data.function,
            "testcases": data.testcases,
            "checker": data.checker,
            "userid": data.userId
        }).execute()

        if not code.data:
            raise HTTPException(status_code=400, detail="Failed to add code")

        return {"message": "Code added successfully", "code": code.data[0]}
    except Exception as e:
        print(f"Error adding code: {e}")
        raise HTTPException(status_code=500, detail="Error adding code")
    
    
@router.delete("/delete/{id}")
async def delete_problem(id: int):
    try:
        delete_codes_result = supabase.table("Problem_code").delete().eq("problemid", id).execute()
     
        
        delete_problem_result = supabase.table("Problem").delete().eq("id", id).execute()
      
        
        return {"message": "Problem and associated codes deleted successfully"}
    except Exception as e:
        print(f"Error deleting problem: {e}")
        raise HTTPException(status_code=500, detail="Error deleting problem")
