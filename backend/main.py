"""
Sahayak Backend - Main FastAPI Application
Provides API endpoints for the Sahayak AI assistant.
"""

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Dict
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import routers
from routers import chat_router, profile_router, eligibility_router, documents_router, application_router, status_router

# Initialize FastAPI app
app = FastAPI(
    title="Sahayak API",
    description="AI-powered assistant for Indian government welfare schemes",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat_router, prefix="/api/v1", tags=["Chat"])
app.include_router(profile_router, prefix="/api/v1", tags=["Profile"])
app.include_router(eligibility_router, prefix="/api/v1", tags=["Eligibility"])
app.include_router(documents_router, prefix="/api/v1", tags=["Documents"])
app.include_router(application_router, prefix="/api/v1", tags=["Application"])
app.include_router(status_router, prefix="/api/v1", tags=["Status"])


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "name": "Sahayak API",
        "version": "1.0.0",
        "description": "AI-powered assistant for Indian government welfare schemes",
        "docs": "/docs",
        "endpoints": {
            "chat": "/api/v1/chat",
            "profile": "/api/v1/profile",
            "eligibility": "/api/v1/eligibility/check",
            "documents": "/api/v1/schemes/{scheme_id}/documents",
            "application": "/api/v1/application/package",
            "status": "/api/v1/status/check"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "sahayak-api",
        "environment": {
            "foundry_endpoint": os.environ.get("FOUNDRY_PROJECT_ENDPOINT", "not_set"),
            "model": os.environ.get("FOUNDRY_MODEL_DEPLOYMENT", "not_set"),
            "bing_enabled": bool(os.environ.get("BING_CONNECTION_ID"))
        }
    }


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom HTTP exception handler"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": exc.detail,
            "status_code": exc.status_code
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """General exception handler"""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "error": "Internal server error",
            "detail": str(exc)
        }
    )


if __name__ == "__main__":
    import uvicorn
    
    # Run with: python main.py
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Enable auto-reload for development
        log_level="info"
    )
