import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

from api.routes import conversation, documents, schemes, status

app = FastAPI(
    title="Sahayak API",
    description="AI-powered government scheme discovery assistant for Indian citizens",
    version="1.0.0",
)

# ---------------------------------------------------------------------------
# CORS
# ---------------------------------------------------------------------------
_raw_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173")
allowed_origins: list[str] = [o.strip() for o in _raw_origins.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Routers
# ---------------------------------------------------------------------------
app.include_router(conversation.router, prefix="/api/conversation")
app.include_router(schemes.router, prefix="/api/schemes")
app.include_router(status.router, prefix="/api/status")
app.include_router(documents.router, prefix="/api/documents")


# ---------------------------------------------------------------------------
# Core endpoints
# ---------------------------------------------------------------------------
@app.get("/health")
async def health_check() -> dict:
    return {"status": "ok", "service": "Sahayak API", "version": "1.0.0"}


@app.get("/")
async def root() -> dict:
    return {"message": "Sahayak API", "docs": "/docs"}


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=True,
    )
