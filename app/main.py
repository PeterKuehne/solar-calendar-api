from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
from app.routers import calendar_router
from app.services.auth import verify_api_key

# Load environment variables
load_dotenv()

# Get port from environment variable with default
port = int(os.environ.get("PORT", 10000))
print(f"Starting server on port {port}")

app = FastAPI(
    title="Solar Calendar API",
    description="API für die Verwaltung von Kalenderterminen für das Solar-Bot Projekt",
    version="1.0.0"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In Produktion einschränken
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(
    calendar_router.router,
    prefix="/api/v1",
    dependencies=[Depends(verify_api_key)]
)

@app.get("/")
async def root():
    return {"message": "Solar Calendar API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=port)
