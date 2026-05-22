"""
Application configuration management
"""

from functools import lru_cache
from typing import Optional


class Settings:
    """Application settings with default values"""

    # Application
    app_name: str = "Enterprise Payload Toolkit"
    app_version: str = "1.0.0"
    environment: str = "development"

    # Backend
    backend_host: str = "0.0.0.0"
    backend_port: int = 8000
    backend_reload: bool = True

    # API
    api_v1_prefix: str = "/api/v1"
    api_title: str = "Enterprise Payload Toolkit API"
    api_description: str = "Secure, local-first developer utility toolkit"

    # CORS
    cors_origins: list[str] = ["http://localhost:8501", "http://localhost:3000", "http://localhost:8000"]
    cors_allow_credentials: bool = True
    cors_allow_methods: list[str] = ["*"]
    cors_allow_headers: list[str] = ["*"]

    # File Upload
    max_upload_size_mb: int = 50
    allowed_extensions: list[str] = [
        ".xml",
        ".json",
        ".yaml",
        ".yml",
        ".log",
        ".txt",
        ".env",
        ".conf",
        ".config",
    ]
    temp_upload_dir: str = "./tmp/uploads"

    # Processing
    max_file_size_bytes: int = 52428800  # 50MB
    chunk_size_bytes: int = 8192
    enable_caching: bool = True
    cache_ttl_seconds: int = 3600

    # Logging
    log_level: str = "INFO"
    log_format: str = "text"  # Changed from json to text for simpler output
    log_file: Optional[str] = None  # Disabled file logging for now

    # Security
    disable_xxe: bool = True
    max_recursion_depth: int = 100
    sanitize_inputs: bool = True

    # Performance
    worker_processes: int = 4
    worker_timeout: int = 300

    # Feature Flags
    enable_xml_toolkit: bool = True
    enable_json_toolkit: bool = True
    enable_log_analyzer: bool = True
    enable_regex_assistant: bool = True
    enable_config_comparator: bool = True

    # Development
    debug: bool = False
    profiling_enabled: bool = False


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance

    Returns:
        Settings instance
    """
    return Settings()

# Made with Bob
