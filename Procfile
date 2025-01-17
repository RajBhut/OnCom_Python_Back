release: pip install prisma && prisma migrate deploy && prisma generate
web: uvicorn api.main:app --host=0.0.0.0 --port=${PORT:-8000}
