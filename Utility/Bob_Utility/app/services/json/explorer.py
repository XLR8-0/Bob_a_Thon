"""
JSON Explorer Service
Navigate and explore JSON document structure
"""

import json
from typing import Dict, Any, List, Optional
from app.services.base import BaseService
from app.core.exceptions import ValidationError, ProcessingError


class JSONExplorer(BaseService):
    """Service for exploring JSON document structure"""
    
    def __init__(self):
        super().__init__()
        self.logger.info("Initialized JSONExplorer")
    
    def get_structure(
        self,
        json_content: str,
        max_depth: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Get hierarchical structure of JSON document
        
        Args:
            json_content: JSON string to analyze
            max_depth: Maximum depth to traverse
            
        Returns:
            Structure as nested dictionary
            
        Raises:
            ValidationError: If JSON is invalid
            ProcessingError: If structure generation fails
        """
        try:
            # Parse JSON
            try:
                data = json.loads(json_content)
            except json.JSONDecodeError as e:
                raise ValidationError(f"Invalid JSON: {str(e)}")
            
            # Build structure
            structure = self._build_structure(data, depth=0, max_depth=max_depth)
            
            self.logger.info("Successfully generated structure")
            return structure
            
        except ValidationError:
            raise
        except Exception as e:
            self.logger.error(f"Structure generation failed: {str(e)}")
            raise ProcessingError(f"Failed to generate structure: {str(e)}")
    
    def _build_structure(
        self,
        data: Any,
        depth: int,
        max_depth: Optional[int],
        path: str = "$"
    ) -> Dict[str, Any]:
        """Build structure node"""
        
        # Check depth limit
        if max_depth is not None and depth > max_depth:
            return {"truncated": True}
        
        node = {
            "path": path,
            "type": type(data).__name__,
            "depth": depth
        }
        
        if isinstance(data, dict):
            node["keys"] = list(data.keys())
            node["key_count"] = len(data)
            node["children"] = {}
            
            for key, value in data.items():
                child_path = f"{path}.{key}"
                node["children"][key] = self._build_structure(
                    value, depth + 1, max_depth, child_path
                )
        
        elif isinstance(data, list):
            node["length"] = len(data)
            node["items"] = []
            
            for idx, item in enumerate(data[:10]):  # Limit to first 10 items
                item_path = f"{path}[{idx}]"
                node["items"].append(self._build_structure(
                    item, depth + 1, max_depth, item_path
                ))
            
            if len(data) > 10:
                node["truncated_items"] = len(data) - 10
        
        elif isinstance(data, str):
            node["length"] = len(data)
            node["preview"] = data[:100] if len(data) > 100 else data
        
        elif isinstance(data, (int, float)):
            node["value"] = data
        
        elif isinstance(data, bool):
            node["value"] = data
        
        elif data is None:
            node["value"] = None
        
        return node
    
    def get_statistics(self, json_content: str) -> Dict[str, Any]:
        """
        Get statistics about JSON document
        
        Args:
            json_content: JSON string to analyze
            
        Returns:
            Dictionary with statistics
        """
        try:
            data = json.loads(json_content)
            
            stats = {
                "total_keys": 0,
                "total_values": 0,
                "max_depth": 0,
                "total_objects": 0,
                "total_arrays": 0,
                "total_strings": 0,
                "total_numbers": 0,
                "total_booleans": 0,
                "total_nulls": 0,
                "unique_keys": set()
            }
            
            def traverse(obj: Any, depth: int):
                stats["max_depth"] = max(stats["max_depth"], depth)
                
                if isinstance(obj, dict):
                    stats["total_objects"] += 1
                    stats["total_keys"] += len(obj)
                    
                    for key, value in obj.items():
                        stats["unique_keys"].add(key)
                        stats["total_values"] += 1
                        traverse(value, depth + 1)
                
                elif isinstance(obj, list):
                    stats["total_arrays"] += 1
                    for item in obj:
                        traverse(item, depth + 1)
                
                elif isinstance(obj, str):
                    stats["total_strings"] += 1
                
                elif isinstance(obj, (int, float)):
                    stats["total_numbers"] += 1
                
                elif isinstance(obj, bool):
                    stats["total_booleans"] += 1
                
                elif obj is None:
                    stats["total_nulls"] += 1
            
            traverse(data, 0)
            
            # Convert set to list for JSON serialization
            stats["unique_keys"] = sorted(list(stats["unique_keys"]))
            stats["unique_key_count"] = len(stats["unique_keys"])
            
            self.logger.info(f"Generated statistics: {stats['total_values']} values")
            return stats
            
        except Exception as e:
            raise ProcessingError(f"Statistics generation failed: {str(e)}")
    
    def flatten(
        self,
        json_content: str,
        separator: str = "."
    ) -> Dict[str, Any]:
        """
        Flatten nested JSON structure
        
        Args:
            json_content: JSON string to flatten
            separator: Separator for nested keys
            
        Returns:
            Flattened dictionary
        """
        try:
            data = json.loads(json_content)
            flattened = self._flatten_dict(data, separator=separator)
            
            self.logger.info("Successfully flattened JSON")
            return flattened
            
        except Exception as e:
            raise ProcessingError(f"Flattening failed: {str(e)}")
    
    def _flatten_dict(
        self,
        d: Any,
        parent_key: str = "",
        separator: str = "."
    ) -> Dict[str, Any]:
        """Recursively flatten nested dictionary"""
        items = []
        
        if isinstance(d, dict):
            for k, v in d.items():
                new_key = f"{parent_key}{separator}{k}" if parent_key else k
                if isinstance(v, (dict, list)):
                    items.extend(self._flatten_dict(v, new_key, separator).items())
                else:
                    items.append((new_key, v))
        
        elif isinstance(d, list):
            for i, item in enumerate(d):
                new_key = f"{parent_key}[{i}]"
                if isinstance(item, (dict, list)):
                    items.extend(self._flatten_dict(item, new_key, separator).items())
                else:
                    items.append((new_key, item))
        else:
            items.append((parent_key, d))
        
        return dict(items)
    
    def unflatten(
        self,
        flattened: Dict[str, Any],
        separator: str = "."
    ) -> Any:
        """
        Unflatten a flattened dictionary back to nested structure
        
        Args:
            flattened: Flattened dictionary
            separator: Separator used in keys
            
        Returns:
            Nested structure
        """
        try:
            result = {}
            
            for key, value in flattened.items():
                parts = key.split(separator)
                current = result
                
                for i, part in enumerate(parts[:-1]):
                    # Handle array indices
                    if '[' in part:
                        base_key, idx = part.split('[')
                        idx = int(idx.rstrip(']'))
                        
                        if base_key not in current:
                            current[base_key] = []
                        
                        # Extend list if needed
                        while len(current[base_key]) <= idx:
                            current[base_key].append({})
                        
                        current = current[base_key][idx]
                    else:
                        if part not in current:
                            current[part] = {}
                        current = current[part]
                
                # Set the final value
                final_key = parts[-1]
                if '[' in final_key:
                    base_key, idx = final_key.split('[')
                    idx = int(idx.rstrip(']'))
                    
                    if base_key not in current:
                        current[base_key] = []
                    
                    while len(current[base_key]) <= idx:
                        current[base_key].append(None)
                    
                    current[base_key][idx] = value
                else:
                    current[final_key] = value
            
            self.logger.info("Successfully unflattened dictionary")
            return result
            
        except Exception as e:
            raise ProcessingError(f"Unflattening failed: {str(e)}")
    
    def get_value_at_path(
        self,
        json_content: str,
        path: str,
        separator: str = "."
    ) -> Optional[Any]:
        """
        Get value at specific path
        
        Args:
            json_content: JSON string
            path: Path to value (e.g., "user.address.city")
            separator: Path separator
            
        Returns:
            Value at path or None if not found
        """
        try:
            data = json.loads(json_content)
            parts = path.split(separator)
            current = data
            
            for part in parts:
                if isinstance(current, dict) and part in current:
                    current = current[part]
                elif isinstance(current, list):
                    try:
                        idx = int(part)
                        current = current[idx]
                    except (ValueError, IndexError):
                        return None
                else:
                    return None
            
            return current
            
        except Exception as e:
            self.logger.error(f"Failed to get value at path: {str(e)}")
            return None


# Made with Bob