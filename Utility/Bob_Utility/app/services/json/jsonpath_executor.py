"""
JSONPath Executor Service
Executes JSONPath queries on JSON documents
"""

from typing import List, Dict, Any, Optional
import json
from jsonpath_ng import parse
from jsonpath_ng.ext import parse as parse_ext
from app.services.base import BaseService
from app.core.exceptions import ValidationError, ProcessingError


class JSONPathExecutor(BaseService):
    """Service for executing JSONPath queries"""
    
    def __init__(self):
        super().__init__()
        self.logger.info("Initialized JSONPathExecutor")
    
    def execute_jsonpath(
        self,
        json_content: str,
        jsonpath_query: str,
        use_extended: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Execute JSONPath query on JSON content
        
        Args:
            json_content: JSON string to query
            jsonpath_query: JSONPath expression to execute
            use_extended: Use extended JSONPath syntax
            
        Returns:
            List of matching values with their paths
            
        Raises:
            ValidationError: If JSON or JSONPath is invalid
            ProcessingError: If execution fails
        """
        try:
            # Parse JSON
            try:
                data = json.loads(json_content)
            except json.JSONDecodeError as e:
                raise ValidationError(f"Invalid JSON: {str(e)}")
            
            # Parse and execute JSONPath
            try:
                if use_extended:
                    jsonpath_expr = parse_ext(jsonpath_query)
                else:
                    jsonpath_expr = parse(jsonpath_query)
                
                matches = jsonpath_expr.find(data)
            except Exception as e:
                raise ValidationError(f"Invalid JSONPath expression: {str(e)}")
            
            # Process results
            results = []
            for idx, match in enumerate(matches):
                result = {
                    "index": idx,
                    "path": str(match.full_path),
                    "value": match.value,
                    "type": type(match.value).__name__
                }
                results.append(result)
            
            self.logger.info(f"JSONPath query returned {len(results)} results")
            return results
            
        except ValidationError:
            raise
        except Exception as e:
            self.logger.error(f"JSONPath execution failed: {str(e)}")
            raise ProcessingError(f"Failed to execute JSONPath: {str(e)}")
    
    def find_by_key(
        self,
        json_content: str,
        key_name: str,
        case_sensitive: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Find all occurrences of a key in JSON
        
        Args:
            json_content: JSON string to search
            key_name: Key name to search for
            case_sensitive: Whether search is case-sensitive
            
        Returns:
            List of matching key-value pairs with paths
        """
        try:
            data = json.loads(json_content)
            results = []
            
            def search_recursive(obj: Any, path: str = "$"):
                if isinstance(obj, dict):
                    for k, v in obj.items():
                        current_path = f"{path}.{k}"
                        
                        # Check if key matches
                        if case_sensitive:
                            matches = k == key_name
                        else:
                            matches = k.lower() == key_name.lower()
                        
                        if matches:
                            results.append({
                                "path": current_path,
                                "key": k,
                                "value": v,
                                "type": type(v).__name__
                            })
                        
                        # Recurse into value
                        search_recursive(v, current_path)
                
                elif isinstance(obj, list):
                    for idx, item in enumerate(obj):
                        search_recursive(item, f"{path}[{idx}]")
            
            search_recursive(data)
            self.logger.info(f"Found {len(results)} occurrences of key '{key_name}'")
            return results
            
        except Exception as e:
            raise ProcessingError(f"Key search failed: {str(e)}")
    
    def find_by_value(
        self,
        json_content: str,
        search_value: Any,
        exact_match: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Find all occurrences of a value in JSON
        
        Args:
            json_content: JSON string to search
            search_value: Value to search for
            exact_match: Whether to use exact matching
            
        Returns:
            List of matching paths and values
        """
        try:
            data = json.loads(json_content)
            results = []
            
            def search_recursive(obj: Any, path: str = "$"):
                if isinstance(obj, dict):
                    for k, v in obj.items():
                        current_path = f"{path}.{k}"
                        
                        # Check if value matches
                        if exact_match:
                            matches = v == search_value
                        else:
                            matches = str(search_value).lower() in str(v).lower()
                        
                        if matches:
                            results.append({
                                "path": current_path,
                                "key": k,
                                "value": v,
                                "type": type(v).__name__
                            })
                        
                        # Recurse
                        search_recursive(v, current_path)
                
                elif isinstance(obj, list):
                    for idx, item in enumerate(obj):
                        current_path = f"{path}[{idx}]"
                        
                        if exact_match:
                            matches = item == search_value
                        else:
                            matches = str(search_value).lower() in str(item).lower()
                        
                        if matches:
                            results.append({
                                "path": current_path,
                                "value": item,
                                "type": type(item).__name__
                            })
                        
                        search_recursive(item, current_path)
            
            search_recursive(data)
            self.logger.info(f"Found {len(results)} occurrences of value")
            return results
            
        except Exception as e:
            raise ProcessingError(f"Value search failed: {str(e)}")
    
    def get_value_at_path(
        self,
        json_content: str,
        path: str
    ) -> Optional[Any]:
        """
        Get value at specific JSONPath
        
        Args:
            json_content: JSON string
            path: JSONPath expression
            
        Returns:
            Value at path or None if not found
        """
        try:
            results = self.execute_jsonpath(json_content, path)
            if results:
                return results[0]["value"]
            return None
        except Exception as e:
            self.logger.error(f"Failed to get value at path: {str(e)}")
            return None
    
    def get_all_paths(
        self,
        json_content: str,
        include_values: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Get all paths in JSON document
        
        Args:
            json_content: JSON string to analyze
            include_values: Include values in results
            
        Returns:
            List of all paths
        """
        try:
            data = json.loads(json_content)
            paths = []
            
            def traverse(obj: Any, path: str = "$"):
                if isinstance(obj, dict):
                    for k, v in obj.items():
                        current_path = f"{path}.{k}"
                        result = {"path": current_path, "type": type(v).__name__}
                        if include_values:
                            result["value"] = v
                        paths.append(result)
                        traverse(v, current_path)
                
                elif isinstance(obj, list):
                    for idx, item in enumerate(obj):
                        current_path = f"{path}[{idx}]"
                        result = {"path": current_path, "type": type(item).__name__}
                        if include_values:
                            result["value"] = item
                        paths.append(result)
                        traverse(item, current_path)
            
            traverse(data)
            self.logger.info(f"Found {len(paths)} paths in JSON")
            return paths
            
        except Exception as e:
            raise ProcessingError(f"Path extraction failed: {str(e)}")
    
    def validate_jsonpath(self, jsonpath_query: str) -> tuple[bool, Optional[str]]:
        """
        Validate JSONPath expression syntax
        
        Args:
            jsonpath_query: JSONPath expression to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            parse_ext(jsonpath_query)
            return True, None
        except Exception as e:
            return False, str(e)


# Made with Bob