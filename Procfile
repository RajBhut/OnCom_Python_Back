release: pip install prisma && prisma generate && prisma migrate deploy
web: uvicorn api.main:app --host=0.0.0.0 --port=${PORT:-8000}