"""
RAG Service - Core retrieval-augmented generation pipeline.
Handles embeddings, vector store operations, and LLM interaction.
"""

import os
import logging
from typing import List, Optional, Dict, Any, Tuple
from pathlib import Path
from datetime import datetime

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.schema import Document

from app.core.config import settings
from app.core.knowledge_base import CROP_DISEASE_DATA, format_disease_document
from app.models.schemas import SourceDocument

logger = logging.getLogger(__name__)


class RAGService:
    """
    Core RAG service managing the full pipeline:
    - Embedding generation  : SentenceTransformers via HuggingFace
    - Vector store          : FAISS (persistent on disk)
    - LLM                   : Google Gemini via LangChain
    - Document ingestion    : PDF → chunks → embeddings → FAISS
    """

    def __init__(self):
        self.embeddings = None
        self.vector_store = None
        self.llm = None
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP,
            separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""],
        )
        self._initialized = False

    # ─── Initialisation ───────────────────────────────────────────────────────

    def initialize(self):
        """Initialize embeddings, vector store, and LLM on first call."""
        if self._initialized:
            return
        logger.info("Initializing RAG Service …")
        self._init_embeddings()
        self._init_vector_store()
        self._init_llm()
        self._initialized = True
        logger.info("RAG Service ready.")

    def _init_embeddings(self):
        """Load SentenceTransformers embedding model (CPU)."""
        try:
            logger.info(f"Loading embedding model: {settings.EMBEDDING_MODEL}")
            self.embeddings = HuggingFaceEmbeddings(
                model_name=settings.EMBEDDING_MODEL,
                model_kwargs={"device": "cpu"},
                encode_kwargs={"normalize_embeddings": True},
            )
            logger.info("Embedding model loaded.")
        except Exception as e:
            logger.error(f"Failed to load embeddings: {e}")
            raise

    def _init_vector_store(self):
        """Load existing FAISS index from disk, or seed a new one."""
        store_path = Path(settings.VECTOR_STORE_PATH)
        index_file = store_path / "index.faiss"

        if index_file.exists():
            try:
                logger.info("Loading existing FAISS vector store …")
                self.vector_store = FAISS.load_local(
                    str(store_path),
                    self.embeddings,
                    allow_dangerous_deserialization=True,
                )
                logger.info(f"Vector store loaded ({self.vector_store.index.ntotal} chunks).")
                return
            except Exception as e:
                logger.warning(f"Could not load existing vector store ({e}). Rebuilding …")

        logger.info("Creating new vector store from built-in knowledge base …")
        self._seed_knowledge_base()

    def _seed_knowledge_base(self):
        """Seed FAISS with all built-in crop disease documents."""
        documents = []
        for d in CROP_DISEASE_DATA:
            doc = Document(
                page_content=format_disease_document(d),
                metadata={
                    "source": d["source"],
                    "crop": d["crop"],
                    "disease": d["disease"],
                    "doc_type": "built-in",
                },
            )
            documents.append(doc)

        chunks = self.text_splitter.split_documents(documents)
        logger.info(f"Seeding vector store with {len(chunks)} chunks.")
        self.vector_store = FAISS.from_documents(chunks, self.embeddings)
        self._save_vector_store()

    def _save_vector_store(self):
        """Persist FAISS index to disk."""
        try:
            self.vector_store.save_local(settings.VECTOR_STORE_PATH)
            logger.info("Vector store saved to disk.")
        except Exception as e:
            logger.error(f"Failed to save vector store: {e}")

    def _init_llm(self):
        """Initialize Gemini LLM via LangChain (uses ChatGoogleGenerativeAI)."""
        key = settings.GEMINI_API_KEY
        if not key or key == "your_gemini_api_key_here":
            logger.warning(
                "GEMINI_API_KEY not configured. "
                "LLM unavailable — fallback mode (returns raw retrieved context)."
            )
            self.llm = None
            return
        try:
            from langchain_google_genai import ChatGoogleGenerativeAI
            self.llm = ChatGoogleGenerativeAI(
                model="gemini-1.5-flash",
                google_api_key=key,
                temperature=0.3,
                convert_system_message_to_human=True,
            )
            logger.info("Gemini 1.5 Flash LLM initialized via LangChain.")
        except Exception as e:
            logger.error(f"Failed to initialize Gemini LLM: {e}")
            self.llm = None

    # ─── Core RAG Steps ───────────────────────────────────────────────────────

    def retrieve(self, query: str, k: int = None) -> List[Tuple[Document, float]]:
        """Semantic similarity search → list of (Document, distance_score)."""
        if not self.vector_store:
            return []
        k = k or settings.TOP_K_RESULTS
        try:
            return self.vector_store.similarity_search_with_score(query, k=k)
        except Exception as e:
            logger.error(f"Retrieval error: {e}")
            return []

    def generate_answer(
        self, question: str, context_docs: List[Tuple[Document, float]]
    ) -> str:
        """Generate a grounded answer from retrieved context."""
        if not context_docs:
            return (
                "I could not find relevant information in the knowledge base for your question.\n\n"
                "Please try rephrasing your question, or consult a local agricultural expert "
                "for personalised advice."
            )

        context = "\n\n".join(
            f"[Source {i}]\n{doc.page_content}"
            for i, (doc, _) in enumerate(context_docs, 1)
        )

        if self.llm is None:
            return self._fallback_response(context_docs)

        prompt = self._build_prompt(question, context)
        try:
            from langchain.schema import HumanMessage
            response = self.llm.invoke([HumanMessage(content=prompt)])
            return response.content
        except Exception as e:
            logger.error(f"LLM generation error: {e}")
            return self._fallback_response(context_docs)

    def _build_prompt(self, question: str, context: str) -> str:
        return f"""You are an expert agricultural assistant specialising in crop diseases.
Your answers must be grounded ONLY in the provided context below.

STRICT RULES:
1. Base every claim on the provided context. Do not invent facts.
2. Never fabricate pesticide names, chemical dosages, or treatment protocols.
3. If the context lacks sufficient information, say so clearly.
4. Always advise the user to consult local agricultural extension officers for
   region-specific chemical treatment recommendations.
5. Format your response clearly with relevant headings (Markdown).

─── RETRIEVED CONTEXT ───────────────────────────────────────────────────────
{context}
─────────────────────────────────────────────────────────────────────────────

USER QUESTION: {question}

Please provide a well-structured, accurate answer using the context above.
Include these sections as applicable:
- **Disease Name & Affected Crop**
- **Symptoms**
- **Causes / Pathogen**
- **Favorable Conditions**
- **Prevention Methods**
- **Recommended Management**
- **References / Sources**

End with: *⚠️ Always consult your local agricultural expert for specific chemical
treatment recommendations.*

ANSWER:"""

    def _fallback_response(self, context_docs: List[Tuple[Document, float]]) -> str:
        """Return formatted retrieved content when LLM is unavailable."""
        best_doc, _ = context_docs[0]
        return (
            f"**Information from Knowledge Base:**\n\n"
            f"{best_doc.page_content}\n\n"
            "---\n"
            "⚠️ *This is a direct excerpt from the agricultural knowledge base. "
            "Configure your Gemini API key for full AI-generated responses.*\n\n"
            "🌿 *Always consult your local agricultural extension service for "
            "specific chemical treatment recommendations.*"
        )

    # ─── Main Pipeline Entry Point ────────────────────────────────────────────

    async def query(self, question: str) -> Dict[str, Any]:
        """
        Full RAG pipeline:
        question → embed → retrieve → generate → return answer + sources
        """
        if not self._initialized:
            self.initialize()

        retrieved = self.retrieve(question)
        answer = self.generate_answer(question, retrieved)

        sources = []
        seen = set()
        for doc, score in retrieved:
            src_name = doc.metadata.get("source", "Agricultural Knowledge Base")
            if src_name not in seen:
                seen.add(src_name)
                sources.append(
                    SourceDocument(
                        content=(
                            doc.page_content[:300] + "…"
                            if len(doc.page_content) > 300
                            else doc.page_content
                        ),
                        source=src_name,
                        page=doc.metadata.get("page"),
                        score=round(float(score), 4),
                    )
                )

        return {
            "answer": answer,
            "sources": sources,
            "retrieved_count": len(retrieved),
        }

    # ─── Document Ingestion ───────────────────────────────────────────────────

    def add_documents_from_pdf(self, file_path: str, filename: str) -> int:
        """
        Extract text from a PDF, chunk it, embed it, and add to FAISS.
        Returns the number of chunks added.
        """
        if not self._initialized:
            self.initialize()

        from pypdf import PdfReader
        import re

        reader = PdfReader(file_path)
        documents: List[Document] = []

        for page_num, page in enumerate(reader.pages, 1):
            raw = page.extract_text()
            if not raw or not raw.strip():
                continue
            text = re.sub(r"\s+", " ", raw).strip()
            documents.append(
                Document(
                    page_content=text,
                    metadata={
                        "source": filename,
                        "page": page_num,
                        "doc_type": "uploaded PDF",
                        "upload_time": datetime.utcnow().isoformat(),
                    },
                )
            )

        if not documents:
            raise ValueError(f"No extractable text found in '{filename}'.")

        chunks = self.text_splitter.split_documents(documents)
        logger.info(f"Adding {len(chunks)} chunks from '{filename}' to vector store.")

        if self.vector_store:
            self.vector_store.add_documents(chunks)
        else:
            self.vector_store = FAISS.from_documents(chunks, self.embeddings)

        self._save_vector_store()
        return len(chunks)

    # ─── Stats ────────────────────────────────────────────────────────────────

    def get_stats(self) -> Dict[str, Any]:
        """Return current vector store and LLM status."""
        if not self._initialized:
            self.initialize()

        try:
            total_chunks = self.vector_store.index.ntotal if self.vector_store else 0
        except Exception:
            total_chunks = 0

        return {
            "total_chunks": total_chunks,
            "llm_available": self.llm is not None,
            "embedding_model": settings.EMBEDDING_MODEL,
            "vector_store_type": "FAISS",
        }


# Global singleton instance
rag_service = RAGService()
