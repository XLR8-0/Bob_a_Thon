"""
JSON Parser Service
Handles JSON parsing, formatting, and validation
"""

import json
from typing import Any, Dict, Optional
from app.services.base import BaseService
from app.core.exceptions import ValidationError, ProcessingError


class JSONParser(BaseService):
    """Service for parsing and formatting JSON"""
    
    def __init__(self):
        super().__init__()
        self.logger.info("Initialized JSONParser")
    
    def format(
        self,
        json_content: str,
        indent: int = 2,
        sort_keys: bool = False,
        ensure_ascii: bool = False
    ) -> str:
        """
        Format and beautify JSON content
        
        Args:
            json_content: JSON string to format
            indent: Number of spaces for indentation
            sort_keys: Whether to sort object keys
            ensure_ascii: Escape non-ASCII characters
            
        Returns:
            Formatted JSON string
            
        Raises:
            ValidationError: If JSON is invalid
            ProcessingError: If formatting fails
        """
        try:
            # Parse JSON
            try:
                data = json.loads(json_content)
            except json.JSONDecodeError as e:
                raise ValidationError(f"Invalid JSON at line {e.lineno}, column {e.colno}: {e.msg}")
            
            # Format JSON
            formatted = json.dumps(
                data,
                indent=indent,
                sort_keys=sort_keys,
                ensure_ascii=ensure_ascii
            )
            
            self.logger.info("Successfully formatted JSON")
            return formatted
            
        except ValidationError:
            raise
        except Exception as e:
            self.logger.error(f"JSON formatting failed: {str(e)}")
            raise ProcessingError(f"Failed to format JSON: {str(e)}")
    
    def validate(self, json_content: str) -> bool:
        """
        Validate JSON syntax
        
        Args:
            json_content: JSON string to validate
            
        Returns:
            True if valid, False otherwise
        """
        try:
            json.loads(json_content)
            self.logger.info("JSON validation successful")
            return True
        except json.JSONDecodeError as e:
            self.logger.warning(f"JSON validation failed: {str(e)}")
            return False
    
    def parse(self, json_content: str) -> Any:
        """
        Parse JSON string to Python object
        
        Args:
            json_content: JSON string to parse
            
        Returns:
            Parsed Python object
            
        Raises:
            ValidationError: If JSON is invalid
        """
        try:
            data = json.loads(json_content)
            self.logger.info("Successfully parsed JSON")
            return data
        except json.JSONDecodeError as e:
            raise ValidationError(f"Invalid JSON at line {e.lineno}, column {e.colno}: {e.msg}")
    
    def minify(self, json_content: str) -> str:
        """
        Minify JSON by removing whitespace
        
        Args:
            json_content: JSON string to minify
            
        Returns:
            Minified JSON string
        """
        try:
            data = json.loads(json_content)
            minified = json.dumps(data, separators=(',', ':'))
            self.logger.info("Successfully minified JSON")
            return minified
        except json.JSONDecodeError as e:
            raise ValidationError(f"Invalid JSON: {str(e)}")
    
    def get_size_info(self, json_content: str) -> Dict[str, Any]:
        """
        Get size information about JSON
        
        Args:
            json_content: JSON string to analyze
            
        Returns:
            Dictionary with size information
        """
        try:
            data = json.loads(json_content)
            formatted = json.dumps(data, indent=2)
            minified = json.dumps(data, separators=(',', ':'))
            
            return {
                "original_size": len(json_content),
                "formatted_size": len(formatted),
                "minified_size": len(minified),
                "compression_ratio": round(len(minified) / len(formatted) * 100, 2)
            }
        except Exception as e:
            raise ProcessingError(f"Failed to get size info: {str(e)}")
    
    def escape_string(self, text: str) -> str:
        """
        Escape string for JSON
        
        Args:
            text: String to escape
            
        Returns:
            Escaped string
        """
        return json.dumps(text)[1:-1]  # Remove surrounding quotes
    
    def unescape_string(self, text: str) -> str:
        """
        Unescape JSON string
        
        Args:
            text: Escaped string
            
        Returns:
            Unescaped string
        """
        return json.loads(f'"{text}"')


# Made with Bob