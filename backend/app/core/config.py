from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    APP_NAME: str = "Crop Disease Knowledge Assistant"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    # API Keys
    GEMINI_API_KEY: str = ""

    # Vector Store — use /tmp on cloud (Render), local path in dev
    VECTOR_STORE_TYPE: str = "faiss"
    VECTOR_STORE_PATH: str = os.getenv("VECTOR_STORE_PATH", "./vector_store")

    # Embedding Model
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"

    # RAG Settings
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    TOP_K_RESULTS: int = 5

    # Upload Settings — use /tmp on cloud
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "./uploads")
    MAX_FILE_SIZE: int = 52428800  # 50MB

    # CORS — allow both Vercel frontend and local dev
    ALLOWED_ORIGINS: str = "http://localhost:5173,http://localhost:3000"

    # Admin
    ADMIN_PASSWORD: str = "admin123"

    @property
    def allowed_origins_list(self) -> List[str]:
        return [o.strip() for o in self.ALLOWED_ORIGINS.split(",")]

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

# Ensure directories exist
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs(settings.VECTOR_STORE_PATH, exist_ok=True)
