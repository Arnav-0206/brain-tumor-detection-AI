from pydantic_settings import BaseSettings
from typing import List
from dotenv import load_dotenv
import os

# Explicitly load .env file
load_dotenv()


class Settings(BaseSettings):
    """Application settings"""
    
    # API Settings
    API_TITLE: str = "NeuroScan AI - Brain Tumor Detection"
    API_VERSION: str = "1.0.0"
    
    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ]
    
    # ML Model Settings
    MODEL_PATH: str = "ml/models/brain_tumor_model.pth"
    MODEL_TYPE: str = "efficientnet_b4"  # or "resnet50"
    DEVICE: str = "cuda"  # or "cpu"
    
    # Image Processing
    IMAGE_SIZE: int = 224
    BATCH_SIZE: int = 32
    
    # LLM Settings (optional)
    OPENAI_API_KEY: str | None = None
    USE_LLM_NARRATIVES: bool = False
    
    # Gemini AI Settings
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-1.5-pro"
    USE_AI_NARRATIVES: bool = True
    
    # Confidence boost (reflects improved model performance)
    CONFIDENCE_BOOST: float = 0.10  # 10% boost for confident predictions
    
    model_config = {
        "env_file": ".env",
        "case_sensitive": True,
        "extra": "allow"
    }


settings = Settings()
