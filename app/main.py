from fastapi import FastAPI
from app.core.database import engine
from app.models.user import Base 
from app.api.v1.auth import router as auth_router 

app = FastAPI(
    title="FastAPI Authentication App",
    description="JWT + PostgreSQL based Authentication API",
    version="0.1.0"
)

# Automatically create all tables in DB (development ke liye; production mein Alembic use karo migrations ke liye)
Base.metadata.create_all(bind=engine)

# Include routers (prefix ke saath)
app.include_router(auth_router, prefix="/api/v1", tags=["auth"])

@app.get("/")
def root():
    return {"message": "FastAPI Auth Server is working! 🚀 Use /api/v1/docs for Swagger"}