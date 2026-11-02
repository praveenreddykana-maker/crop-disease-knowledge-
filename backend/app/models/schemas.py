from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
import uuid


# ─── Chat Models ────────────────────────────────────────────────────────────

class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    sources: Optional[List[Dict[str, Any]]] = None


class ChatRequest(BaseModel):
    question: str
    conversation_id: Optional[str] = None
    session_id: Optional[str] = None


class SourceDocument(BaseModel):
    content: str
    source: str
    page: Optional[int] = None
    score: Optional[float] = None


class ChatResponse(BaseModel):
    answer: str
    sources: List[SourceDocument] = []
    conversation_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)


# ─── Conversation Models ─────────────────────────────────────────────────────

class Conversation(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str = ""
    messages: List[ChatMessage] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class ConversationSummary(BaseModel):
    id: str
    title: str
    message_count: int
    created_at: datetime
    updated_at: datetime
    last_message: Optional[str] = None


# ─── Document Models ─────────────────────────────────────────────────────────

class DocumentInfo(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    filename: str
    original_name: str
    file_type: str
    file_size: int
    upload_time: datetime = Field(default_factory=datetime.utcnow)
    status: str = "processing"  # processing, indexed, error
    chunk_count: int = 0
    error_message: Optional[str] = None


class DocumentUploadResponse(BaseModel):
    success: bool
    message: str
    document: Optional[DocumentInfo] = None


class KnowledgeBaseStats(BaseModel):
    total_documents: int
    total_chunks: int
    indexed_documents: int
    processing_documents: int
    failed_documents: int
    vector_store_size: int


# ─── Admin Models ────────────────────────────────────────────────────────────

class AdminLoginRequest(BaseModel):
    password: str


class AdminLoginResponse(BaseModel):
    success: bool
    token: Optional[str] = None
    message: str

