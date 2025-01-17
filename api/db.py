from prisma import Prisma
from contextlib import asynccontextmanager

@asynccontextmanager
async def get_prisma():
    prisma = Prisma()
    await prisma.connect()
    try:
        yield prisma
    finally:
        await prisma.disconnect()


prisma = Prisma()