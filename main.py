from fastapi import FastAPI, HTTPException
from prisma import Prisma

app = FastAPI()
prisma = Prisma()

@app.on_event("startup")
async def startup():
    await prisma.connect()

@app.on_event("shutdown")
async def shutdown():
    await prisma.disconnect()

@app.post("/users/")
async def create_user(email: str, name: str = None):
    user = await prisma.user.create(
        data={
            "email": email,
            "name": name,
        }
    )
    return user
@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    user = await prisma.user.find_unique(where={"id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user