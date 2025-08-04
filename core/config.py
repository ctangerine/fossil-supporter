import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

# Get the project root directory (be folder)
BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    CELERY_BROKER_URL: str
    GOOGLE_API_KEY: str
    REDIS_URL: str
    LANGSMITH_TRACING: bool = False
    LANGSMITH_ENDPOINT: str = ""
    LANGSMITH_API_KEY: str = ""
    LANGSMITH_PROJECT: str = ""

    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    model_config = SettingsConfigDict(
        # Thử load từ .env file trước (cho local development)
        env_file=BASE_DIR / ".env" if (BASE_DIR / ".env").exists() else None,
        env_file_encoding='utf-8',
        # Environment variables sẽ override values từ .env file
        case_sensitive=True,
        # Cho phép lấy từ system environment variables
        extra='ignore'
    )

    @classmethod
    def create_settings(cls):
        """
        Factory method để tạo settings với fallback logic
        """
        # Kiểm tra xem có đang chạy trên Railway không
        is_railway = os.getenv('RAILWAY_ENVIRONMENT') is not None
        
        if is_railway:
            print("Running on Railway - using environment variables")
        else:
            env_file_path = BASE_DIR / ".env"
            if env_file_path.exists():
                print(f"Running locally - using .env file: {env_file_path}")
            else:
                print("Running locally - using environment variables (no .env file found)")
        
        return cls()

# Tạo instance settings
settings = Settings.create_settings()

# Export các giá trị để backward compatibility
LANGSMITH_TRACING = settings.LANGSMITH_TRACING
LANGSMITH_ENDPOINT = settings.LANGSMITH_ENDPOINT
LANGSMITH_API_KEY = settings.LANGSMITH_API_KEY
LANGSMITH_PROJECT = settings.LANGSMITH_PROJECT
GOOGLE_API_KEY = settings.GOOGLE_API_KEY
CELERY_BROKER_URL = settings.CELERY_BROKER_URL
REDIS_URL = settings.REDIS_URL
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

# Debug function để kiểm tra config
def debug_settings():
    """
    Function để debug settings - chỉ dùng khi cần thiết
    """
    print("=== Settings Debug ===")
    print(f"Railway Environment: {os.getenv('RAILWAY_ENVIRONMENT', 'Not set')}")
    print(f"GOOGLE_API_KEY: {'***' + GOOGLE_API_KEY[-4:] if GOOGLE_API_KEY and len(GOOGLE_API_KEY) > 4 else 'NOT SET'}")
    print(f"REDIS_URL: {REDIS_URL}")
    print(f"CELERY_BROKER_URL: {CELERY_BROKER_URL}")
    print(f"LANGSMITH_TRACING: {LANGSMITH_TRACING}")
    print(f"SECRET_KEY: {'***' + SECRET_KEY[-4:] if SECRET_KEY and len(SECRET_KEY) > 4 else 'NOT SET'}")
    print("=====================")

# Uncomment dòng dưới để debug khi cần
# debug_settings()