"""
Chat API router - handles all chatbot interactions via the RAG pipeline.
"""

import uuid
import logging
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from app.models.schemas import ChatRequest, ChatResponse, ChatMessage
from app.services.rag_service import rag_service
from app.services.chat_history_service import chat_history_service

router = APIRouter(prefix="/api/chat", tags=["Chat"])
logger = logging.getLogger(__name__)


@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Main RAG-powered chat endpoint.
    Retrieves relevant context from the vector store and generates an answer.
    """
    if not request.question or not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    question = request.question.strip()

    try:
        # Get or create conversation
        conv = chat_history_service.get_or_create(request.conversation_id, question)

        # Add user message to history
        user_message = ChatMessage(role="user", content=question)
        chat_history_service.add_message(conv.id, user_message)

        # Run RAG pipeline
        result = await rag_service.query(question)

        # Add assistant message to history
        assistant_message = ChatMessage(
            role="assistant",
            content=result["answer"],
            sources=[s.model_dump() for s in result["sources"]],
        )
        chat_history_service.add_message(conv.id, assistant_message)

        return ChatResponse(
            answer=result["answer"],
            sources=result["sources"],
            conversation_id=conv.id,
        )

    except Exception as e:
        logger.error(f"Chat error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"An error occurred while processing your question: {str(e)}")


@router.get("/history")
async def get_chat_history():
    """Return list of all conversations."""
    conversations = chat_history_service.list_conversations()
    return {"conversations": [c.model_dump(mode="json") for c in conversations]}


@router.get("/history/search")
async def search_history(q: str):
    """Search through chat history."""
    results = chat_history_service.search_conversations(q)
    return {"results": [r.model_dump(mode="json") for r in results]}


@router.get("/history/{conversation_id}")
async def get_conversation(conversation_id: str):
    """Get full conversation by ID."""
    conv = chat_history_service.get_conversation(conversation_id)
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found.")
    return conv.model_dump(mode="json")


@router.delete("/history/{conversation_id}")
async def delete_conversation(conversation_id: str):
    """Delete a specific conversation."""
    success = chat_history_service.delete_conversation(conversation_id)
    if not success:
        raise HTTPException(status_code=404, detail="Conversation not found.")
    return {"message": "Conversation deleted successfully."}


@router.delete("/history")
async def clear_all_history():
    """Clear all chat history."""
    chat_history_service.clear_all()
    return {"message": "All chat history cleared."}

