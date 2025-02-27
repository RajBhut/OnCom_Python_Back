
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
class Submision(BaseModel):
    lan:str
    code:str
class NotesData(BaseModel):
    edge: str
    node: str
    
class Room(BaseModel):
    name:str
    title:str

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
async def update_problem_notes(id: int, data: NotesData, current_user=Depends(get_current_user)):
    try:
        print(data)
        updated_problem = supabase.table("notes").upsert(
            {
                "problem_id": id,
                "user_id": current_user["id"],
                "edgedata": data.edge,
                "nodedata": data.node
            },
            on_conflict="user_id,problem_id"        ).execute()
       

        if not updated_problem.data:
            raise HTTPException(status_code=400, detail="Failed to update problem")

        return updated_problem.data[0]
    except Exception as e:
        print(f"Error updating problem notes: {e}")
        raise HTTPException(status_code=500, detail="Error updating problem notes")

@router.get("/update/{id}")
async def get_problem_by_id(id: int, current_user=Depends(get_current_user)):
    try:
        problem = supabase.table("notes").select("*").eq("problem_id", id).eq("user_id",current_user["id"]).execute()
     
        return problem.data[0] if problem.data else {}
    except Exception as e:
        print(f"Error fetching problem by ID: {e}")
        raise HTTPException(status_code=500, detail="Error fetching problem by ID")

@router.get("/des/{id}")
async def get_des_by_id(id: int):
    try:
        problem = supabase.table("Problem").select("*").eq("id", id).execute()
     
        return problem.data[0] if problem.data else {}
    except Exception as e:
        print(f"Error fetching problem by ID: {e}")
        raise HTTPException(status_code=500, detail="Error fetching problem by ID")



@router.post("/solved/{id}")
async def mark_problem_solved(id: int, Sub:Submision, current_user=Depends(get_current_user)):
    
    try:
        updated_problem = supabase.table("Solved").upsert({
    "probid": id,
    "userid": current_user["id"],  
    "code": Sub.code,  
    "lan": Sub.lan  }).execute() 
       
        
        if not updated_problem:
            raise HTTPException(status_code=400, detail="Failed to mark problem as solved")

        return updated_problem.data[0]
    except Exception as e:
        print(f"Error marking problem as solved: {e}")
        raise HTTPException(status_code=500, detail="Error marking problem as solved")
    
@router.get("/solved")
async def get_solved_problems(current_user=Depends(get_current_user)):
    try:
        solved = supabase.table("Solved").select("probid").eq("userid", current_user["id"]).execute()
        
        if not solved.data:
            return []
        
        problem_ids = [item["probid"] for item in solved.data]
        
        problems = supabase.table("Problem").select("*").in_("id", problem_ids).execute()
        
        return problems.data or []
        
    except Exception as e:
        print(f"Error fetching solved problems: {e}")
        raise HTTPException(status_code=500, detail="Error fetching solved problems")
@router.get("/solved/{id}")
async def check_solved_problem(id: int, current_user=Depends(get_current_user)):
    try:
        solved = supabase.table("Solved").select("*").eq("userid", current_user["id"]).eq("probid", id).execute()
        
        if not solved.data:
            return []
        return solved.data
        
        
    except Exception as e:
        print(f"Error checking solved problem: {e}")
        raise HTTPException(status_code=500, detail="Error checking solved problem")   
    
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
    


@router.post("/room")
async def create_room(room:Room, current_user = Depends(get_current_user)):
    try:
        room = supabase.table("rooms").insert({
            "name": room.name,
            "title": room.title,
            "user_id": current_user["id"]
        }).execute()
        if not room.data:
            raise HTTPException(status_code=400, detail="Failed to create room")
        return {"message": "Room created successfully", "room": room.data[0]}
    except Exception as e:
        print(f"Error creating room: {e}")
        raise HTTPException(status_code=500, detail="Error creating room")

@router.get("/room")
async def get_rooms(current_user = Depends(get_current_user)):
    try:
        rooms = supabase.table("rooms").select("*").execute()
        return rooms.data
    except Exception as e:
        print(f"Error fetching rooms: {e}")
        raise HTTPException(status_code=500, detail="Error fetching rooms")


@router.delete("/room/{id}")
async def delete_room(id:str, current_user = Depends(get_current_user)):
    try:
        room = supabase.table("rooms").delete().eq("name", id).execute()
        return {"message": "Room deleted successfully"}
    except Exception as e:
        print(f"Error deleting room: {e}")
        raise HTTPException(status_code=500, detail="Error deleting room")



@router.delete("/delete/{id}")
async def delete_problem(id: int):
    try:
        delete_codes_result = supabase.table("Problem_code").delete().eq("problemid", id).execute()
     
        
        delete_problem_result = supabase.table("Problem").delete().eq("id", id).execute()
      
        
        return {"message": "Problem and associated codes deleted successfully"}
    except Exception as e:
        print(f"Error deleting problem: {e}")
        raise HTTPException(status_code=500, detail="Error deleting problem")


