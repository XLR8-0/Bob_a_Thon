"""
CSV Converter Service
Converts CSV to/from JSON and other formats
"""

import csv
import json
import io
from typing import List, Dict, Any, Optional
from app.services.base import BaseService
from app.core.exceptions import ValidationError, ProcessingError


class CSVConverter(BaseService):
    """Service for converting CSV to/from other formats"""
    
    def __init__(self):
        super().__init__()
        self.logger.info("Initialized CSVConverter")
    
    def json_to_csv(
        self,
        json_content: str,
        delimiter: str = ",",
        include_header: bool = True
    ) -> str:
        """
        Convert JSON to CSV
        
        Args:
            json_content: JSON string (array of objects)
            delimiter: CSV delimiter
            include_header: Whether to include header row
            
        Returns:
            CSV string
        """
        try:
            # Parse JSON
            try:
                data = json.loads(json_content)
            except json.JSONDecodeError as e:
                raise ValidationError(f"Invalid JSON: {str(e)}")
            
            # Ensure data is a list
            if not isinstance(data, list):
                raise ValidationError("JSON must be an array of objects")
            
            if not data:
                return ""
            
            # Get all unique keys from all objects
            all_keys = set()
            for item in data:
                if isinstance(item, dict):
                    all_keys.update(item.keys())
            
            fieldnames = sorted(list(all_keys))
            
            # Create CSV
            output = io.StringIO()
            writer = csv.DictWriter(
                output,
                fieldnames=fieldnames,
                delimiter=delimiter,
                quoting=csv.QUOTE_MINIMAL
            )
            
            if include_header:
                writer.writeheader()
            
            for item in data:
                if isinstance(item, dict):
                    writer.writerow(item)
            
            csv_str = output.getvalue()
            self.logger.info("Successfully converted JSON to CSV")
            return csv_str
            
        except ValidationError:
            raise
        except Exception as e:
            self.logger.error(f"JSON to CSV conversion failed: {str(e)}")
            raise ProcessingError(f"Failed to convert JSON to CSV: {str(e)}")
    
    def csv_to_json(
        self,
        csv_content: str,
        delimiter: str = ",",
        pretty: bool = True,
        indent: int = 2
    ) -> str:
        """
        Convert CSV to JSON
        
        Args:
            csv_content: CSV string
            delimiter: CSV delimiter
            pretty: Whether to format JSON with indentation
            indent: Number of spaces for indentation
            
        Returns:
            JSON string (array of objects)
        """
        try:
            # Parse CSV
            input_stream = io.StringIO(csv_content)
            reader = csv.DictReader(input_stream, delimiter=delimiter)
            
            # Convert to list of dicts
            data = []
            for row in reader:
                # Convert empty strings to None for cleaner JSON
                cleaned_row = {
                    k: (v if v != "" else None)
                    for k, v in row.items()
                }
                data.append(cleaned_row)
            
            # Convert to JSON
            if pretty:
                json_str = json.dumps(data, indent=indent, ensure_ascii=False)
            else:
                json_str = json.dumps(data, ensure_ascii=False)
            
            self.logger.info("Successfully converted CSV to JSON")
            return json_str
            
        except Exception as e:
            self.logger.error(f"CSV to JSON conversion failed: {str(e)}")
            raise ProcessingError(f"Failed to convert CSV to JSON: {str(e)}")
    
    def get_sample_json(self) -> str:
        """Get sample JSON data for testing"""
        sample = [
            {
                "id": 1,
                "name": "John Doe",
                "email": "john@example.com",
                "age": 30,
                "city": "New York"
            },
            {
                "id": 2,
                "name": "Jane Smith",
                "email": "jane@example.com",
                "age": 25,
                "city": "Los Angeles"
            },
            {
                "id": 3,
                "name": "Bob Johnson",
                "email": "bob@example.com",
                "age": 35,
                "city": "Chicago"
            }
        ]
        return json.dumps(sample, indent=2)
    
    def get_sample_csv(self) -> str:
        """Get sample CSV data for testing"""
        return """id,name,email,age,city
1,John Doe,john@example.com,30,New York
2,Jane Smith,jane@example.com,25,Los Angeles
3,Bob Johnson,bob@example.com,35,Chicago"""


# Made with Bob