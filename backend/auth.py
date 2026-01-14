from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from db_manager import create_user_if_not_exists
import time

router = APIRouter()

# Schema
class GoogleLoginRequest(BaseModel):
    id: str
    email: str
    name: str = "User"
    picture: str = ""

@router.post("/auth/google")
def google_login(req: GoogleLoginRequest):
    """
    Handle Google Login (or Simulation).
    In a real app, we would verify the ID Token here using google-auth library.
    Since we don't have keys, we trust the client (for this demo/personal use).
    """
    
    # 1. Create or Update User in DB
    user_data = {
        "id": req.id,
        "email": req.email,
        "name": req.name,
        "picture": req.picture
    }
    
    success = create_user_if_not_exists(user_data)
    
    if not success:
        return {"status": "error", "message": "DB Error"}
        
    from db_manager import get_user
    real_user = get_user(req.id)
    
    if not real_user:
        # Fallback if fetch failed but create succeeded (unlikely)
        real_user = user_data

    return {
        "status": "success",
        "user": real_user,
        "token": f"mock_token_{req.id}_{int(time.time())}" # Simulation
    }
