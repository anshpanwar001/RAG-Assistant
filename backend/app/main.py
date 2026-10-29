"""
The FastAPI application entry point.

Stage 1 only adds a health-check endpoint. Monitoring tools and deployment
platforms call endpoints like this to confirm the server is alive.
"""

from fastapi import FastAPI

from app.config import get_settings

app = FastAPI(title="RAG Assistant API", version="0.1.0")


@app.get("/health")
def health() -> dict[str, str]:
    """Return a simple status message. It does not expose any secrets."""
    settings = get_settings()
    return {
        "status": "ok",
        "model": settings.gemini_model,
    }