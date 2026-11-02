"""
Admin API router - authentication and admin-specific operations.
"""

import logging
from fastapi import APIRouter, HTTPException

from app.core.config import settings
from app.models.schemas import AdminLoginRequest, AdminLoginResponse
from app.services.rag_service import rag_service

router = APIRouter(prefix="/api/admin", tags=["Admin"])
logger = logging.getLogger(__name__)


@router.post("/login", response_model=AdminLoginResponse)
async def admin_login(request: AdminLoginRequest):
    """Authenticate as admin."""
    if request.password == settings.ADMIN_PASSWORD:
        return AdminLoginResponse(
            success=True,
            token=settings.ADMIN_PASSWORD,  # Simple token = password for this demo
            message="Login successful.",
        )
    raise HTTPException(status_code=401, detail="Invalid admin password.")


@router.get("/health")
async def health_check():
    """System health check."""
    rag_stats = rag_service.get_stats()
    return {
        "status": "healthy",
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "rag": rag_stats,
    }


@router.post("/rebuild-index")
async def rebuild_knowledge_base(password: str):
    """Rebuild the vector store from scratch (admin only)."""
    if password != settings.ADMIN_PASSWORD:
        raise HTTPException(status_code=403, detail="Admin authentication required.")

    try:
        rag_service.vector_store = None
        rag_service._initialized = False
        rag_service.initialize()
        return {"message": "Knowledge base rebuilt successfully from built-in data."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Rebuild failed: {str(e)}")

