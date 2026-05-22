"""
Base parser class for all parsers in the Enterprise Payload Toolkit
"""

from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

from app.core.logger import LoggerMixin

T = TypeVar("T")


class ParserBase(ABC, LoggerMixin, Generic[T]):
    """
    Abstract base class for all parsers

    This class provides a common interface for parsing different formats
    (XML, JSON, YAML, etc.) with consistent error handling and logging.
    """

    def __init__(self) -> None:
        """Initialize the parser"""
        self.logger.info(f"Initialized {self.__class__.__name__}")

    @abstractmethod
    def parse(self, content: str) -> T:
        """
        Parse content and return parsed object

        Args:
            content: String content to parse

        Returns:
            Parsed object of type T

        Raises:
            ParsingError: If parsing fails
        """
        pass

    @abstractmethod
    def validate(self, content: str) -> bool:
        """
        Validate content without full parsing

        Args:
            content: String content to validate

        Returns:
            True if valid, False otherwise
        """
        pass

    @abstractmethod
    def format(self, content: str, **kwargs: Any) -> str:
        """
        Format/beautify content

        Args:
            content: String content to format
            **kwargs: Additional formatting options

        Returns:
            Formatted content string

        Raises:
            ProcessingError: If formatting fails
        """
        pass

    def safe_parse(self, content: str, default: Any = None) -> T | Any:
        """
        Safely parse content, returning default on error

        Args:
            content: String content to parse
            default: Default value to return on error

        Returns:
            Parsed object or default value
        """
        try:
            return self.parse(content)
        except Exception as e:
            self.logger.warning(f"Safe parse failed: {e}")
            return default

    def get_parser_info(self) -> dict[str, Any]:
        """
        Get information about this parser

        Returns:
            Dictionary with parser information
        """
        return {
            "name": self.__class__.__name__,
            "type": self.__class__.__bases__[0].__name__,
            "module": self.__class__.__module__,
        }

# Made with Bob
