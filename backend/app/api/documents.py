"""
Documents API router - handles document uploads and knowledge base management.
Admin-protected endpoints.
"""

import os
import uuid
import logging
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, HTTPException, UploadFile, File, Header
import aiofiles

from app.core.config import settings
from app.models.schemas import DocumentUploadResponse, KnowledgeBaseStats
from app.services.document_service import document_service
from app.services.rag_service import rag_service

router = APIRouter(prefix="/api/documents", tags=["Documents"])
logger = logging.getLogger(__name__)


def verify_admin(x_admin_token: Optional[str] = None) -> bool:
    """Simple admin token verification."""
    return x_admin_token == settings.ADMIN_PASSWORD


@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    x_admin_token: Optional[str] = Header(None),
):
    """
    Upload a PDF document to the knowledge base.
    Requires admin authentication.
    """
    if not verify_admin(x_admin_token):
        raise HTTPException(status_code=403, detail="Admin authentication required.")

    # Read file content
    content = await file.read()
    file_size = len(content)

    # Validate file
    error = document_service.validate_file(file.filename, file_size)
    if error:
        raise HTTPException(status_code=400, detail=error)

    # Generate unique filename
    ext = Path(file.filename).suffix
    unique_filename = f"{uuid.uuid4()}{ext}"
    file_path = Path(settings.UPLOAD_DIR) / unique_filename

    # Register document
    doc_info = document_service.register_document(
        filename=unique_filename,
        original_name=file.filename,
        file_size=file_size,
    )

    # Save file
    try:
        async with aiofiles.open(file_path, "wb") as f:
            await f.write(content)
    except Exception as e:
        document_service.update_status(doc_info.id, "error", error_message=str(e))
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")

    # Process and index in background
    try:
        chunk_count = rag_service.add_documents_from_pdf(str(file_path), file.filename)
        document_service.update_status(doc_info.id, "indexed", chunk_count=chunk_count)
        doc_info.status = "indexed"
        doc_info.chunk_count = chunk_count
    except Exception as e:
        logger.error(f"Error indexing document: {e}", exc_info=True)
        document_service.update_status(doc_info.id, "error", error_message=str(e))
        doc_info.status = "error"
        doc_info.error_message = str(e)

    return DocumentUploadResponse(
        success=doc_info.status == "indexed",
        message=f"Document '{file.filename}' uploaded and indexed with {doc_info.chunk_count} chunks."
        if doc_info.status == "indexed"
        else f"Document uploaded but indexing failed: {doc_info.error_message}",
        document=doc_info,
    )


@router.get("/")
async def list_documents(x_admin_token: Optional[str] = Header(None)):
    """List all uploaded documents (admin only)."""
    if not verify_admin(x_admin_token):
        raise HTTPException(status_code=403, detail="Admin authentication required.")
    docs = document_service.get_all_documents()
    return {"documents": [d.model_dump(mode="json") for d in docs]}


@router.delete("/{doc_id}")
async def delete_document(doc_id: str, x_admin_token: Optional[str] = Header(None)):
    """Delete an uploaded document (admin only)."""
    if not verify_admin(x_admin_token):
        raise HTTPException(status_code=403, detail="Admin authentication required.")
    success = document_service.delete_document(doc_id)
    if not success:
        raise HTTPException(status_code=404, detail="Document not found.")
    return {"message": "Document deleted successfully."}


@router.get("/stats/knowledge-base")
async def get_knowledge_base_stats(x_admin_token: Optional[str] = Header(None)):
    """Get knowledge base statistics (admin only)."""
    if not verify_admin(x_admin_token):
        raise HTTPException(status_code=403, detail="Admin authentication required.")

    doc_stats = document_service.get_stats()
    rag_stats = rag_service.get_stats()

    return KnowledgeBaseStats(
        total_documents=doc_stats["total_documents"],
        total_chunks=rag_stats.get("total_chunks", 0),
        indexed_documents=doc_stats["indexed_documents"],
        processing_documents=doc_stats["processing_documents"],
        failed_documents=doc_stats["failed_documents"],
        vector_store_size=rag_stats.get("total_chunks", 0),
    )

