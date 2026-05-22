"""
Base validator class for all validators in the Enterprise Payload Toolkit
"""

from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

from app.core.logger import LoggerMixin

T = TypeVar("T")


class ValidationResult:
    """Result of a validation operation"""

    def __init__(
        self,
        is_valid: bool,
        errors: list[str] | None = None,
        warnings: list[str] | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        self.is_valid = is_valid
        self.errors = errors or []
        self.warnings = warnings or []
        self.details = details or {}

    def to_dict(self) -> dict[str, Any]:
        """Convert validation result to dictionary"""
        return {
            "is_valid": self.is_valid,
            "errors": self.errors,
            "warnings": self.warnings,
            "details": self.details,
        }

    def __bool__(self) -> bool:
        """Allow using ValidationResult in boolean context"""
        return self.is_valid

    def __repr__(self) -> str:
        status = "Valid" if self.is_valid else "Invalid"
        error_count = len(self.errors)
        warning_count = len(self.warnings)
        return f"ValidationResult({status}, errors={error_count}, warnings={warning_count})"


class ValidatorBase(ABC, LoggerMixin, Generic[T]):
    """
    Abstract base class for all validators

    This class provides a common interface for validating different formats
    with consistent error handling and reporting.
    """

    def __init__(self) -> None:
        """Initialize the validator"""
        self.logger.info(f"Initialized {self.__class__.__name__}")

    @abstractmethod
    def validate(self, content: T, **kwargs: Any) -> ValidationResult:
        """
        Validate content

        Args:
            content: Content to validate
            **kwargs: Additional validation options

        Returns:
            ValidationResult object
        """
        pass

    def validate_string(self, content: str, **kwargs: Any) -> ValidationResult:
        """
        Validate string content (convenience method)

        Args:
            content: String content to validate
            **kwargs: Additional validation options

        Returns:
            ValidationResult object
        """
        return self.validate(content, **kwargs)  # type: ignore

    def is_valid(self, content: T, **kwargs: Any) -> bool:
        """
        Check if content is valid (simple boolean check)

        Args:
            content: Content to validate
            **kwargs: Additional validation options

        Returns:
            True if valid, False otherwise
        """
        result = self.validate(content, **kwargs)
        return result.is_valid

    def get_errors(self, content: T, **kwargs: Any) -> list[str]:
        """
        Get validation errors

        Args:
            content: Content to validate
            **kwargs: Additional validation options

        Returns:
            List of error messages
        """
        result = self.validate(content, **kwargs)
        return result.errors

    def get_warnings(self, content: T, **kwargs: Any) -> list[str]:
        """
        Get validation warnings

        Args:
            content: Content to validate
            **kwargs: Additional validation options

        Returns:
            List of warning messages
        """
        result = self.validate(content, **kwargs)
        return result.warnings

    def get_validator_info(self) -> dict[str, Any]:
        """
        Get information about this validator

        Returns:
            Dictionary with validator information
        """
        return {
            "name": self.__class__.__name__,
            "type": self.__class__.__bases__[0].__name__,
            "module": self.__class__.__module__,
        }

# Made with Bob
