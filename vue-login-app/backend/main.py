from fastapi import FastAPI, Header, HTTPException
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client, Client
import os
from pathlib import Path
from dotenv import load_dotenv
import uvicorn


# Find your previously created .env in the "2026.Genesix" folder (2 levels up)
env_path = Path(__file__).resolve().parent.parent.parent / '.env'

# Load environment variables from that specific .env file
load_dotenv(dotenv_path=env_path)

# Global variable to hold the client
supabase: Client = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize Supabase
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    
    if not url or not key:
        print("⚠️ Warning: SUPABASE_URL or SUPABASE_KEY not found in .env")
        # You might want to raise an error here in production
        # raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in your .env file")
        
    global supabase
    if url and key:
        supabase = create_client(url, key)
        print("✅ Supabase connected!")
    
    yield
    
    # Shutdown: Clean up resources if needed
    print("🛑 Supabase connection closed.")

app = FastAPI(lifespan=lifespan)

# Allow CORS so Vue can talk to it
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_root():
    return {"message": "Supabase is ready"}

@app.get("/api/user")
async def get_current_user(authorization: str = Header(None)):
    global supabase
    if not supabase:
        raise HTTPException(status_code=500, detail="Supabase not initialized")
        
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid authorization header")
        
    # Extract the token from "Bearer <token>"
    token = authorization.split(" ")[1]
    
    try:
        # Pass the token to Supabase to verify it securely on the server side
        user_response = await supabase.auth.get_user(token)
        
        # Return the verified user's email back to the Vue frontend
        return {"email": user_response.user.email}
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Authentication failed: {str(e)}")

@app.get("/api/data")
async def fetch_data():
    global supabase
    if not supabase:
        return {"error": "Supabase client not initialized"}
        
    try:
        response = supabase.table("profiles").select("*").limit(5).execute()
        return {"success": True, "data": response.data}
    except Exception as e:
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    # IMPORTANT: To use this directly, change your directory to the backend folder first!
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
