"""
Demo FastAPI app for auto-fix bot testing
Railway deployment target
"""
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Demo API", version="1.0.0")


class HealthResponse(BaseModel):
    status: str
    environment: str


class UserData(BaseModel):
    username: str
    email: str


@app.get("/")
async def root():
    """Basic health check endpoint"""
    return {"message": "FastAPI demo app is running", "status": "ok"}


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check with environment info
    """
    env = os.environ.get("ENVIRONMENT", "development")
    return HealthResponse(
        status="healthy",
        environment=env
    )


@app.post("/api/users")
async def create_user(user: UserData):
    """
    Create a new user - requires API key validation
    
    SEEDED BUG: Reads required env var without fallback/check
    This will throw KeyError at request time (not import time)
    """
    # This line will fail if API_SECRET_KEY is not set
    api_key = os.environ["API_SECRET_KEY"]  # BUG: No .get() or try/except
    
    # Simulate some validation logic
    if not api_key:
        raise HTTPException(status_code=500, detail="API key not configured")
    
    # In a real app, this would save to a database
    return {
        "message": "User created successfully",
        "user": user.dict(),
        "validated": True
    }


@app.get("/api/config")
async def get_config():
    """
    Returns sanitized config info
    """
    return {
        "app_name": "Demo FastAPI App",
        "version": "1.0.0",
        "debug_mode": os.environ.get("DEBUG", "false"),
        "allowed_origins": os.environ.get("ALLOWED_ORIGINS", "*")
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
