"""
JSON Schema Generator and Validator Service
Generates JSON schemas from data and validates JSON against schemas
"""

import json
from typing import Any, Dict, List, Optional
from app.services.base import BaseService
from app.core.exceptions import ValidationError, ProcessingError


class JSONSchemaGenerator(BaseService):
    """Service for generating and validating JSON schemas"""
    
    def __init__(self):
        super().__init__()
        self.logger.info("Initialized JSONSchemaGenerator")
    
    def generate_schema(
        self,
        json_content: str,
        title: Optional[str] = None,
        description: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate JSON schema from JSON data
        
        Args:
            json_content: JSON string to analyze
            title: Optional schema title
            description: Optional schema description
            
        Returns:
            JSON schema as dictionary
            
        Raises:
            ValidationError: If JSON is invalid
            ProcessingError: If schema generation fails
        """
        try:
            # Parse JSON
            try:
                data = json.loads(json_content)
            except json.JSONDecodeError as e:
                raise ValidationError(f"Invalid JSON: {str(e)}")
            
            # Generate schema
            schema = {
                "$schema": "http://json-schema.org/draft-07/schema#",
                "type": self._get_type(data)
            }
            
            if title:
                schema["title"] = title
            if description:
                schema["description"] = description
            
            # Add type-specific properties
            if isinstance(data, dict):
                schema["properties"] = {}
                schema["required"] = []
                
                for key, value in data.items():
                    schema["properties"][key] = self._generate_property_schema(value)
                    schema["required"].append(key)
            
            elif isinstance(data, list) and data:
                schema["items"] = self._generate_property_schema(data[0])
            
            self.logger.info("Successfully generated JSON schema")
            return schema
            
        except ValidationError:
            raise
        except Exception as e:
            self.logger.error(f"Schema generation failed: {str(e)}")
            raise ProcessingError(f"Failed to generate schema: {str(e)}")
    
    def _generate_property_schema(self, value: Any) -> Dict[str, Any]:
        """Generate schema for a property value"""
        schema = {"type": self._get_type(value)}
        
        if isinstance(value, dict):
            schema["properties"] = {}
            for k, v in value.items():
                schema["properties"][k] = self._generate_property_schema(v)
        
        elif isinstance(value, list) and value:
            schema["items"] = self._generate_property_schema(value[0])
        
        elif isinstance(value, str):
            schema["minLength"] = 0
        
        elif isinstance(value, (int, float)):
            schema["minimum"] = 0
        
        return schema
    
    def _get_type(self, value: Any) -> str:
        """Get JSON schema type for a value"""
        if value is None:
            return "null"
        elif isinstance(value, bool):
            return "boolean"
        elif isinstance(value, int):
            return "integer"
        elif isinstance(value, float):
            return "number"
        elif isinstance(value, str):
            return "string"
        elif isinstance(value, list):
            return "array"
        elif isinstance(value, dict):
            return "object"
        else:
            return "string"
    
    def validate_against_schema(
        self,
        json_content: str,
        schema: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Validate JSON against a schema (basic validation)
        
        Args:
            json_content: JSON string to validate
            schema: JSON schema dictionary
            
        Returns:
            Validation result with errors if any
        """
        try:
            data = json.loads(json_content)
            errors = []
            
            # Basic type validation
            expected_type = schema.get("type")
            actual_type = self._get_type(data)
            
            if expected_type and expected_type != actual_type:
                errors.append({
                    "path": "$",
                    "message": f"Expected type '{expected_type}', got '{actual_type}'"
                })
            
            # Validate object properties
            if isinstance(data, dict) and "properties" in schema:
                errors.extend(self._validate_object(data, schema, "$"))
            
            # Validate array items
            if isinstance(data, list) and "items" in schema:
                errors.extend(self._validate_array(data, schema, "$"))
            
            return {
                "valid": len(errors) == 0,
                "errors": errors,
                "error_count": len(errors)
            }
            
        except Exception as e:
            raise ProcessingError(f"Validation failed: {str(e)}")
    
    def _validate_object(
        self,
        data: Dict[str, Any],
        schema: Dict[str, Any],
        path: str
    ) -> List[Dict[str, str]]:
        """Validate object against schema"""
        errors = []
        properties = schema.get("properties", {})
        required = schema.get("required", [])
        
        # Check required properties
        for req in required:
            if req not in data:
                errors.append({
                    "path": f"{path}.{req}",
                    "message": f"Required property '{req}' is missing"
                })
        
        # Validate each property
        for key, value in data.items():
            if key in properties:
                prop_schema = properties[key]
                expected_type = prop_schema.get("type")
                actual_type = self._get_type(value)
                
                if expected_type and expected_type != actual_type:
                    errors.append({
                        "path": f"{path}.{key}",
                        "message": f"Expected type '{expected_type}', got '{actual_type}'"
                    })
                
                # Recursive validation for nested objects
                if isinstance(value, dict) and "properties" in prop_schema:
                    errors.extend(self._validate_object(value, prop_schema, f"{path}.{key}"))
        
        return errors
    
    def _validate_array(
        self,
        data: List[Any],
        schema: Dict[str, Any],
        path: str
    ) -> List[Dict[str, str]]:
        """Validate array against schema"""
        errors = []
        items_schema = schema.get("items", {})
        expected_type = items_schema.get("type")
        
        for idx, item in enumerate(data):
            actual_type = self._get_type(item)
            
            if expected_type and expected_type != actual_type:
                errors.append({
                    "path": f"{path}[{idx}]",
                    "message": f"Expected type '{expected_type}', got '{actual_type}'"
                })
        
        return errors
    
    def infer_types(self, json_content: str) -> Dict[str, Any]:
        """
        Infer data types from JSON
        
        Args:
            json_content: JSON string to analyze
            
        Returns:
            Dictionary with type information
        """
        try:
            data = json.loads(json_content)
            
            def analyze_value(value: Any, path: str = "$") -> Dict[str, Any]:
                result = {
                    "path": path,
                    "type": self._get_type(value),
                    "nullable": value is None
                }
                
                if isinstance(value, dict):
                    result["properties"] = {}
                    for k, v in value.items():
                        result["properties"][k] = analyze_value(v, f"{path}.{k}")
                
                elif isinstance(value, list):
                    if value:
                        result["item_type"] = self._get_type(value[0])
                        result["length"] = len(value)
                    else:
                        result["item_type"] = "unknown"
                        result["length"] = 0
                
                elif isinstance(value, str):
                    result["length"] = len(value)
                
                return result
            
            return analyze_value(data)
            
        except Exception as e:
            raise ProcessingError(f"Type inference failed: {str(e)}")


# Made with Bob