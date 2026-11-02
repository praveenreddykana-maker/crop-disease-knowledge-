"""
Document Service - manages uploaded documents and their metadata.
"""

import os
import json
import uuid
import logging
from typing import List, Optional, Dict
from pathlib import Path
from datetime import datetime

from app.core.config import settings
from app.models.schemas import DocumentInfo

logger = logging.getLogger(__name__)

METADATA_FILE = Path(settings.UPLOAD_DIR) / "documents_metadata.json"
ALLOWED_EXTENSIONS = {".pdf"}
MAX_FILE_SIZE = settings.MAX_FILE_SIZE


class DocumentService:
    """Manages uploaded documents and their indexing status."""

    def __init__(self):
        self._documents: Dict[str, DocumentInfo] = {}
        self._load_metadata()

    def _load_metadata(self):
        """Load document metadata from disk."""
        if METADATA_FILE.exists():
            try:
                with open(METADATA_FILE, "r") as f:
                    data = json.load(f)
                for doc_data in data:
                    doc = DocumentInfo(**doc_data)
                    self._documents[doc.id] = doc
                logger.info(f"Loaded metadata for {len(self._documents)} documents.")
            except Exception as e:
                logger.error(f"Error loading document metadata: {e}")
                self._documents = {}

    def _save_metadata(self):
        """Persist document metadata to disk."""
        try:
            data = [doc.model_dump(mode="json") for doc in self._documents.values()]
            with open(METADATA_FILE, "w") as f:
                json.dump(data, f, indent=2, default=str)
        except Exception as e:
            logger.error(f"Error saving document metadata: {e}")

    def validate_file(self, filename: str, file_size: int) -> Optional[str]:
        """
        Validate file before processing.
        Returns error message if invalid, None if valid.
        """
        ext = Path(filename).suffix.lower()
        if ext not in ALLOWED_EXTENSIONS:
            return f"File type '{ext}' is not supported. Only PDF files are allowed."
        if file_size > MAX_FILE_SIZE:
            max_mb = MAX_FILE_SIZE // (1024 * 1024)
            return f"File size exceeds the maximum allowed size of {max_mb}MB."
        return None

    def register_document(self, filename: str, original_name: str, file_size: int) -> DocumentInfo:
        """Register a new document and return its info."""
        doc = DocumentInfo(
            id=str(uuid.uuid4()),
            filename=filename,
            original_name=original_name,
            file_type="PDF",
            file_size=file_size,
            status="processing",
        )
        self._documents[doc.id] = doc
        self._save_metadata()
        return doc

    def update_status(
        self,
        doc_id: str,
        status: str,
        chunk_count: int = 0,
        error_message: Optional[str] = None,
    ):
        """Update document processing status."""
        if doc_id in self._documents:
            self._documents[doc_id].status = status
            self._documents[doc_id].chunk_count = chunk_count
            if error_message:
                self._documents[doc_id].error_message = error_message
            self._save_metadata()

    def get_all_documents(self) -> List[DocumentInfo]:
        """Return all documents sorted by upload time (newest first)."""
        return sorted(
            self._documents.values(),
            key=lambda d: d.upload_time,
            reverse=True,
        )

    def get_document(self, doc_id: str) -> Optional[DocumentInfo]:
        return self._documents.get(doc_id)

    def delete_document(self, doc_id: str) -> bool:
        """Delete a document's metadata and its file."""
        doc = self._documents.get(doc_id)
        if not doc:
            return False

        # Delete the file
        file_path = Path(settings.UPLOAD_DIR) / doc.filename
        if file_path.exists():
            try:
                file_path.unlink()
            except Exception as e:
                logger.error(f"Error deleting file {file_path}: {e}")

        del self._documents[doc_id]
        self._save_metadata()
        return True

    def get_stats(self) -> dict:
        docs = list(self._documents.values())
        return {
            "total_documents": len(docs),
            "indexed_documents": sum(1 for d in docs if d.status == "indexed"),
            "processing_documents": sum(1 for d in docs if d.status == "processing"),
            "failed_documents": sum(1 for d in docs if d.status == "error"),
            "total_chunks": sum(d.chunk_count for d in docs),
        }


# Global singleton
document_service = DocumentService()

