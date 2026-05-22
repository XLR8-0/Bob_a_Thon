"""
Base service class for all services in the Enterprise Payload Toolkit
"""

from abc import ABC
from typing import Any

from app.core.logger import LoggerMixin


class BaseService(ABC, LoggerMixin):
    """
    Abstract base class for all services

    Provides common functionality like logging and error handling
    """

    def __init__(self) -> None:
        """Initialize the service"""
        self.logger.info(f"Initialized {self.__class__.__name__}")

    def get_service_info(self) -> dict[str, Any]:
        """
        Get information about this service

        Returns:
            Dictionary with service information
        """
        return {
            "name": self.__class__.__name__,
            "module": self.__class__.__module__,
            "type": "service",
        }

# Made with Bob
