from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    APP_NAME: str = "Crop Disease Knowledge Assistant"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    # API Keys
    GEMINI_API_KEY: str = ""

    # Vector Store
    VECTOR_STORE_TYPE: str = "faiss"
    VECTOR_STORE_PATH: str = "./vector_store"

    # Embedding Model
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"

    # RAG Settings
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    TOP_K_RESULTS: int = 5

    # Upload Settings
    UPLOAD_DIR: str = "./uploads"
    MAX_FILE_SIZE: int = 52428800  # 50MB

    # CORS
    ALLOWED_ORIGINS: str = "http://localhost:3000,http://localhost:5173"

    # Admin
    ADMIN_PASSWORD: str = "admin123"

    @property
    def allowed_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

# Ensure directories exist
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs(settings.VECTOR_STORE_PATH, exist_ok=True)

