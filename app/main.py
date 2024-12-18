from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.models import APIKey, APIKeyIn
from fastapi.openapi.models import SecurityScheme
from dotenv import load_dotenv
import os
from app.routers import calendar_router
from app.services.auth import verify_api_key

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Solar Calendar API",
    description="API für die Verwaltung von Kalenderterminen für das Solar-Bot Projekt",
    version="1.0.0"
)

# API Key Security Schema
app.openapi_schema = None  # Reset schema to ensure updates
app.swagger_ui_init_oauth = {}
app.openapi_components = {
    "securitySchemes": {
        "ApiKeyAuth": {
            "type": "apiKey",
            "in": "header",
            "name": "X-API-Key"
        }
    }
}
app.openapi_security = [{"ApiKeyAuth": []}]

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
