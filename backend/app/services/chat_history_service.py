"""
Chat History Service - manages conversation history in-memory and on disk.
"""

import json
import uuid
import logging
from typing import List, Optional, Dict
from pathlib import Path
from datetime import datetime

from app.models.schemas import Conversation, ChatMessage, ConversationSummary

logger = logging.getLogger(__name__)

HISTORY_FILE = Path("./data/chat_history.json")


class ChatHistoryService:
    """Manages user conversation history."""

    def __init__(self):
        self._conversations: Dict[str, Conversation] = {}
        HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
        self._load()

    def _load(self):
        if HISTORY_FILE.exists():
            try:
                with open(HISTORY_FILE, "r") as f:
                    data = json.load(f)
                for conv_data in data:
                    conv = Conversation(**conv_data)
                    self._conversations[conv.id] = conv
                logger.info(f"Loaded {len(self._conversations)} conversations from history.")
            except Exception as e:
                logger.error(f"Error loading chat history: {e}")

    def _save(self):
        try:
            data = [c.model_dump(mode="json") for c in self._conversations.values()]
            with open(HISTORY_FILE, "w") as f:
                json.dump(data, f, indent=2, default=str)
        except Exception as e:
            logger.error(f"Error saving chat history: {e}")

    def create_conversation(self, first_question: str = "") -> Conversation:
        conv = Conversation(
            id=str(uuid.uuid4()),
            title=first_question[:60] + "..." if len(first_question) > 60 else first_question,
            messages=[],
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        self._conversations[conv.id] = conv
        self._save()
        return conv

    def get_or_create(self, conversation_id: Optional[str], question: str) -> Conversation:
        if conversation_id and conversation_id in self._conversations:
            return self._conversations[conversation_id]
        return self.create_conversation(question)

    def add_message(self, conversation_id: str, message: ChatMessage):
        conv = self._conversations.get(conversation_id)
        if conv:
            conv.messages.append(message)
            conv.updated_at = datetime.utcnow()
            self._save()

    def get_conversation(self, conversation_id: str) -> Optional[Conversation]:
        return self._conversations.get(conversation_id)

    def list_conversations(self) -> List[ConversationSummary]:
        summaries = []
        for conv in sorted(self._conversations.values(), key=lambda c: c.updated_at, reverse=True):
            last_msg = conv.messages[-1].content if conv.messages else None
            summaries.append(
                ConversationSummary(
                    id=conv.id,
                    title=conv.title,
                    message_count=len(conv.messages),
                    created_at=conv.created_at,
                    updated_at=conv.updated_at,
                    last_message=last_msg[:100] + "..." if last_msg and len(last_msg) > 100 else last_msg,
                )
            )
        return summaries

    def search_conversations(self, query: str) -> List[ConversationSummary]:
        query_lower = query.lower()
        results = []
        for conv in self._conversations.values():
            if query_lower in conv.title.lower() or any(
                query_lower in msg.content.lower() for msg in conv.messages
            ):
                last_msg = conv.messages[-1].content if conv.messages else None
                results.append(
                    ConversationSummary(
                        id=conv.id,
                        title=conv.title,
                        message_count=len(conv.messages),
                        created_at=conv.created_at,
                        updated_at=conv.updated_at,
                        last_message=last_msg,
                    )
                )
        return results

    def delete_conversation(self, conversation_id: str) -> bool:
        if conversation_id in self._conversations:
            del self._conversations[conversation_id]
            self._save()
            return True
        return False

    def clear_all(self):
        self._conversations = {}
        self._save()


# Global singleton
chat_history_service = ChatHistoryService()

