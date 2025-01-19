# from prisma import Prisma
# from contextlib import asynccontextmanager

# @asynccontextmanager
# async def get_prisma():
#     prisma = Prisma()
#     await prisma.connect()
#     try:
#         yield prisma
#     finally:
#         await prisma.disconnect()


# prisma = Prisma()

from supabase import create_client, Client
import os
from dotenv import load_dotenv
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")


if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Supabase URL or Key not set in environment variables.")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
