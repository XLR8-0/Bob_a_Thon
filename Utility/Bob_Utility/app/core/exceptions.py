"""
Custom exceptions for the Enterprise Payload Toolkit
"""

from typing import Any, Dict, Optional


class BaseToolkitException(Exception):
    """Base exception for all toolkit errors"""

    def __init__(
        self,
        message: str,
        error_code: str = "TOOLKIT_ERROR",
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.message = message
        self.error_code = error_code
        self.details = details or {}
        super().__init__(self.message)

    def to_dict(self) -> Dict[str, Any]:
        """Convert exception to dictionary for API responses"""
        return {
            "status": "error",
            "error_code": self.error_code,
            "message": self.message,
            "details": self.details,
        }


class ValidationError(BaseToolkitException):
    """Raised when input validation fails"""

    def __init__(
        self, message: str, details: Optional[Dict[str, Any]] = None
    ) -> None:
        super().__init__(
            message=message, error_code="VALIDATION_ERROR", details=details
        )


class ParsingError(BaseToolkitException):
    """Raised when parsing fails"""

    def __init__(
        self, message: str, details: Optional[Dict[str, Any]] = None
    ) -> None:
        super().__init__(message=message, error_code="PARSING_ERROR", details=details)


class ProcessingError(BaseToolkitException):
    """Raised when processing fails"""

    def __init__(
        self, message: str, details: Optional[Dict[str, Any]] = None
    ) -> None:
        super().__init__(
            message=message, error_code="PROCESSING_ERROR", details=details
        )


class ResourceError(BaseToolkitException):
    """Raised when resource operations fail"""

    def __init__(
        self, message: str, details: Optional[Dict[str, Any]] = None
    ) -> None:
        super().__init__(message=message, error_code="RESOURCE_ERROR", details=details)


class XMLParsingError(ParsingError):
    """Raised when XML parsing fails"""

    def __init__(
        self, message: str, details: Optional[Dict[str, Any]] = None
    ) -> None:
        super().__init__(message=f"XML Parsing Error: {message}", details=details)


class JSONParsingError(ParsingError):
    """Raised when JSON parsing fails"""

    def __init__(
        self, message: str, details: Optional[Dict[str, Any]] = None
    ) -> None:
        super().__init__(message=f"JSON Parsing Error: {message}", details=details)


class YAMLParsingError(ParsingError):
    """Raised when YAML parsing fails"""

    def __init__(
        self, message: str, details: Optional[Dict[str, Any]] = None
    ) -> None:
        super().__init__(message=f"YAML Parsing Error: {message}", details=details)


class XPathError(ProcessingError):
    """Raised when XPath execution fails"""

    def __init__(
        self, message: str, details: Optional[Dict[str, Any]] = None
    ) -> None:
        super().__init__(message=f"XPath Error: {message}", details=details)


class JSONPathError(ProcessingError):
    """Raised when JSONPath execution fails"""

    def __init__(
        self, message: str, details: Optional[Dict[str, Any]] = None
    ) -> None:
        super().__init__(message=f"JSONPath Error: {message}", details=details)


class SchemaValidationError(ValidationError):
    """Raised when schema validation fails"""

    def __init__(
        self, message: str, details: Optional[Dict[str, Any]] = None
    ) -> None:
        super().__init__(message=f"Schema Validation Error: {message}", details=details)


class FileSizeError(ResourceError):
    """Raised when file size exceeds limits"""

    def __init__(
        self, message: str, details: Optional[Dict[str, Any]] = None
    ) -> None:
        super().__init__(message=f"File Size Error: {message}", details=details)


class FileTypeError(ValidationError):
    """Raised when file type is not allowed"""

    def __init__(
        self, message: str, details: Optional[Dict[str, Any]] = None
    ) -> None:
        super().__init__(message=f"File Type Error: {message}", details=details)


class RegexError(ProcessingError):
    """Raised when regex operations fail"""

    def __init__(
        self, message: str, details: Optional[Dict[str, Any]] = None
    ) -> None:
        super().__init__(message=f"Regex Error: {message}", details=details)


class ConfigComparisonError(ProcessingError):
    """Raised when config comparison fails"""

    def __init__(
        self, message: str, details: Optional[Dict[str, Any]] = None
    ) -> None:
        super().__init__(
            message=f"Config Comparison Error: {message}", details=details
        )

# Made with Bob
