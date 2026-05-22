"""
Text Converter Service
Converts text case and provides text statistics
"""

from typing import Dict, Any
from app.services.base import BaseService
from app.core.exceptions import ValidationError


class TextConverter(BaseService):
    """Service for text case conversion and statistics"""
    
    def __init__(self):
        super().__init__()
        self.logger.info("Initialized TextConverter")
    
    def to_lower_case(self, text: str) -> str:
        """Convert text to lowercase"""
        try:
            result = text.lower()
            self.logger.info("Successfully converted text to lowercase")
            return result
        except Exception as e:
            self.logger.error(f"Lowercase conversion failed: {str(e)}")
            raise ValidationError(f"Failed to convert to lowercase: {str(e)}")
    
    def to_upper_case(self, text: str) -> str:
        """Convert text to uppercase"""
        try:
            result = text.upper()
            self.logger.info("Successfully converted text to uppercase")
            return result
        except Exception as e:
            self.logger.error(f"Uppercase conversion failed: {str(e)}")
            raise ValidationError(f"Failed to convert to uppercase: {str(e)}")
    
    def to_proper_case(self, text: str) -> str:
        """Convert text to proper case (title case)"""
        try:
            result = text.title()
            self.logger.info("Successfully converted text to proper case")
            return result
        except Exception as e:
            self.logger.error(f"Proper case conversion failed: {str(e)}")
            raise ValidationError(f"Failed to convert to proper case: {str(e)}")
    
    def get_text_statistics(self, text: str) -> Dict[str, Any]:
        """
        Get text statistics
        
        Returns:
            Dictionary with character count, word count, and line count
        """
        try:
            # Character count (including spaces)
            char_count = len(text)
            
            # Character count (excluding spaces)
            char_count_no_spaces = len(text.replace(" ", "").replace("\n", "").replace("\t", ""))
            
            # Word count
            words = text.split()
            word_count = len(words)
            
            # Line count
            lines = text.split('\n')
            line_count = len(lines)
            
            stats = {
                "characters": char_count,
                "characters_no_spaces": char_count_no_spaces,
                "words": word_count,
                "lines": line_count
            }
            
            self.logger.info("Successfully calculated text statistics")
            return stats
            
        except Exception as e:
            self.logger.error(f"Text statistics calculation failed: {str(e)}")
            raise ValidationError(f"Failed to calculate text statistics: {str(e)}")
    
    def convert_case(self, text: str, case_type: str) -> Dict[str, Any]:
        """
        Convert text case and return result with statistics
        
        Args:
            text: Text to convert
            case_type: Type of case conversion (lower, upper, proper)
            
        Returns:
            Dictionary with converted text and statistics
        """
        try:
            if not text:
                raise ValidationError("Text content is required")
            
            # Convert based on case type
            if case_type.lower() == "lower":
                converted_text = self.to_lower_case(text)
            elif case_type.lower() == "upper":
                converted_text = self.to_upper_case(text)
            elif case_type.lower() == "proper":
                converted_text = self.to_proper_case(text)
            else:
                raise ValidationError(f"Invalid case type: {case_type}. Use 'lower', 'upper', or 'proper'")
            
            # Get statistics
            stats = self.get_text_statistics(converted_text)
            
            return {
                "converted_text": converted_text,
                "statistics": stats,
                "case_type": case_type.lower()
            }
            
        except ValidationError:
            raise
        except Exception as e:
            self.logger.error(f"Case conversion failed: {str(e)}")
            raise ValidationError(f"Failed to convert case: {str(e)}")


# Made with Bob