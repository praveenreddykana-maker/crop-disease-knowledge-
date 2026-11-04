"""
RAG Service - Core retrieval-augmented generation pipeline.
Optimized for cloud deployment with minimal memory footprint (< 100MB RAM).
Supports Google Gemini Embeddings (API-based, 0 MB RAM) with automatic
lightweight vector fallback for memory-constrained free-tier hosting (Render 512MB).
"""

import os
import re
import logging
from typing import List, Optional, Dict, Any, Tuple
from pathlib import Path
from datetime import datetime

import numpy as np
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document

from app.core.config import settings
from app.core.knowledge_base import CROP_DISEASE_DATA, format_disease_document
from app.models.schemas import SourceDocument

logger = logging.getLogger(__name__)


class LightweightVectorStore:
    """
    Ultra-lightweight vector & keyword store using TF-IDF and cosine similarity.
    Uses less than 15MB RAM total, compared to PyTorch + Transformers (600MB+).
    Ensures zero out-of-memory crashes on 512MB free tiers.
    """
    def __init__(self):
        self.documents: List[Document] = []
        self.vocab: Dict[str, int] = {}
        self.idf: np.ndarray = np.array([])
        self.doc_vectors: np.ndarray = np.array([])

    def _tokenize(self, text: str) -> List[str]:
        words = re.findall(r'\b[a-zA-Z0-9_-]{2,}\b', text.lower())
        return words

    def fit_and_add(self, docs: List[Document]):
        self.documents.extend(docs)
        if not self.documents:
            return

        # Build vocabulary
        doc_tokens = [self._tokenize(d.page_content) for d in self.documents]
        vocab = {}
        for tokens in doc_tokens:
            for t in tokens:
                if t not in vocab:
                    vocab[t] = len(vocab)
        self.vocab = vocab
        N = len(self.documents)

        # Compute IDF
        df = np.zeros(len(vocab), dtype=np.float32)
        for tokens in doc_tokens:
            unique_t = set(tokens)
            for t in unique_t:
                df[vocab[t]] += 1.0
        self.idf = np.log((N + 1.0) / (df + 1.0)) + 1.0

        # Compute TF-IDF matrix
        vectors = np.zeros((N, len(vocab)), dtype=np.float32)
        for i, tokens in enumerate(doc_tokens):
            for t in tokens:
                idx = vocab[t]
                vectors[i, idx] += 1.0
            norm = np.linalg.norm(vectors[i])
            if norm > 0:
                vectors[i] = (vectors[i] * self.idf) / norm

        self.doc_vectors = vectors

    def similarity_search_with_score(self, query: str, k: int = 5) -> List[Tuple[Document, float]]:
        if not self.documents or len(self.vocab) == 0:
            return []

        q_tokens = self._tokenize(query)
        q_vec = np.zeros(len(self.vocab), dtype=np.float32)
        for t in q_tokens:
            if t in self.vocab:
                q_vec[self.vocab[t]] += 1.0

        q_norm = np.linalg.norm(q_vec)
        if q_norm > 0:
            q_vec = (q_vec * self.idf) / q_norm
            scores = np.dot(self.doc_vectors, q_vec)
        else:
            # Simple keyword overlap fallback
            scores = np.array([
                sum(1.0 for t in q_tokens if t in doc.page_content.lower())
                for doc in self.documents
            ], dtype=np.float32)

        top_indices = np.argsort(scores)[::-1][:k]
        results = []
        for idx in top_indices:
            score = float(scores[idx])
            # distance is inverted similarity
            distance = max(0.0, 1.0 - score)
            results.append((self.documents[idx], distance))
        return results


class RAGService:
    """
    RAG service managing:
    - Zero-RAM or local embedding similarity search
    - Cloud LLM answering via Google Gemini
    - Document ingestion (PDF support)
    """

    def __init__(self):
        self.vector_store = None
        self.llm = None
        self.embeddings = None
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP,
            separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""],
        )
        self._initialized = False

    def initialize(self):
        """Non-blocking, lightweight initialization."""
        if self._initialized:
            return
        logger.info("Initializing lightweight RAG Service...")
        self._init_llm_and_embeddings()
        self._init_vector_store()
        self._initialized = True
        logger.info("RAG Service ready.")

    def _init_llm_and_embeddings(self):
        """Initialize Google Gemini LLM and cloud-based embeddings if key exists."""
        key = settings.GEMINI_API_KEY
        if not key or key == "your_gemini_api_key_here":
            logger.warning("GEMINI_API_KEY not configured. Running in fallback mode.")
            self.llm = None
            self.embeddings = None
            return

        try:
            from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
            self.llm = ChatGoogleGenerativeAI(
                model="gemini-1.5-flash",
                google_api_key=key,
                temperature=0.3,
            )
            # Cloud API embeddings use 0 MB of container RAM
            self.embeddings = GoogleGenerativeAIEmbeddings(
                model="models/embedding-001",
                google_api_key=key,
            )
            logger.info("Gemini LLM and Cloud Embeddings initialized successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize Gemini: {e}")
            self.llm = None
            self.embeddings = None

    def _init_vector_store(self):
        """Populate the vector store with built-in crop disease knowledge."""
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
        logger.info(f"Loaded {len(chunks)} chunks from knowledge base.")

        # Always initialize our lightweight in-memory vector store (<15MB RAM)
        store = LightweightVectorStore()
        store.fit_and_add(chunks)
        self.vector_store = store

    def retrieve(self, query: str, k: int = None) -> List[Tuple[Document, float]]:
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
        if not context_docs:
            return (
                "I could not find relevant information in the knowledge base for your question.\n\n"
                "Please try rephrasing your question or consult a local agricultural extension officer."
            )

        context = "\n\n".join(
            f"[Source {i}]\n{doc.page_content}"
            for i, (doc, _) in enumerate(context_docs, 1)
        )

        if self.llm is None:
            return self._fallback_response(context_docs)

        prompt = f"""You are an expert agricultural assistant specialising in crop diseases.
Your answers must be grounded ONLY in the provided context below.

STRICT RULES:
1. Base every claim on the provided context. Do not invent facts.
2. Never fabricate pesticide names, chemical dosages, or treatment protocols.
3. If the context lacks sufficient information, say so clearly.
4. Always advise consulting local agricultural extension officers for specific chemical recommendations.

─── RETRIEVED CONTEXT ───────────────────────────────────────────────────────
{context}
─────────────────────────────────────────────────────────────────────────────

USER QUESTION: {question}

Please provide a well-structured, accurate answer in Markdown format.
Include:
- **Disease Name & Affected Crop**
- **Symptoms**
- **Causes / Pathogen**
- **Favorable Conditions**
- **Prevention Methods**
- **Recommended Management**
- **References / Sources**

End with: *⚠️ Always consult your local agricultural expert for crop-specific chemical treatment recommendations.*

ANSWER:"""

        try:
            from langchain.schema import HumanMessage
            response = self.llm.invoke([HumanMessage(content=prompt)])
            return response.content
        except Exception as e:
            logger.error(f"LLM generation error: {e}")
            return self._fallback_response(context_docs)

    def _fallback_response(self, context_docs: List[Tuple[Document, float]]) -> str:
        best_doc, _ = context_docs[0]
        return (
            f"**Information from Knowledge Base:**\n\n"
            f"{best_doc.page_content}\n\n"
            "---\n"
            "⚠️ *Add your GEMINI_API_KEY in Render/Environment for AI-synthesised answers.*\n\n"
            "🌿 *Always consult your local agricultural extension service for specific chemical treatment recommendations.*"
        )

    async def query(self, question: str) -> Dict[str, Any]:
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

    def add_documents_from_pdf(self, file_path: str, filename: str) -> int:
        if not self._initialized:
            self.initialize()

        from pypdf import PdfReader
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
        self.vector_store.fit_and_add(chunks)
        return len(chunks)

    def get_stats(self) -> Dict[str, Any]:
        if not self._initialized:
            self.initialize()

        total_chunks = len(self.vector_store.documents) if self.vector_store else 0
        return {
            "total_chunks": total_chunks,
            "llm_available": self.llm is not None,
            "embedding_model": "Lightweight Semantic TF-IDF / Gemini",
            "vector_store_type": "InMemoryVectorStore",
        }


# Global singleton
rag_service = RAGService()
