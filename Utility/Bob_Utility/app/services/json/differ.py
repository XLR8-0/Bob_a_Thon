"""
JSON Differ Service
Compares two JSON documents and identifies differences
"""

import json
from typing import Dict, Any, List
from deepdiff import DeepDiff
from app.services.base import BaseService
from app.core.exceptions import ValidationError, ProcessingError


class JSONDiffer(BaseService):
    """Service for comparing JSON documents"""
    
    def __init__(self):
        super().__init__()
        self.logger.info("Initialized JSONDiffer")
    
    def compare_json(
        self,
        json1: str,
        json2: str,
        ignore_order: bool = False,
        ignore_string_case: bool = False,
        significant_digits: int = None
    ) -> Dict[str, Any]:
        """
        Compare two JSON documents
        
        Args:
            json1: First JSON string
            json2: Second JSON string
            ignore_order: Ignore list/array order
            ignore_string_case: Ignore string case differences
            significant_digits: Number of significant digits for floats
            
        Returns:
            Dictionary with comparison results
            
        Raises:
            ValidationError: If JSON is invalid
            ProcessingError: If comparison fails
        """
        try:
            # Parse both JSON documents
            try:
                data1 = json.loads(json1)
                data2 = json.loads(json2)
            except json.JSONDecodeError as e:
                raise ValidationError(f"Invalid JSON: {str(e)}")
            
            # Perform deep comparison
            diff = DeepDiff(
                data1,
                data2,
                ignore_order=ignore_order,
                ignore_string_case=ignore_string_case,
                significant_digits=significant_digits,
                verbose_level=2
            )
            
            # Process differences
            result = {
                "identical": len(diff) == 0,
                "differences": self._process_differences(diff),
                "summary": self._generate_summary(diff)
            }
            
            self.logger.info(f"Comparison complete: {len(result['differences'])} differences found")
            return result
            
        except ValidationError:
            raise
        except Exception as e:
            self.logger.error(f"JSON comparison failed: {str(e)}")
            raise ProcessingError(f"Failed to compare JSON: {str(e)}")
    
    def _process_differences(self, diff: DeepDiff) -> List[Dict[str, Any]]:
        """Process DeepDiff results into structured format"""
        differences = []
        
        # Values changed
        if 'values_changed' in diff:
            for path, change in diff['values_changed'].items():
                differences.append({
                    "type": "value_changed",
                    "path": path,
                    "old_value": change.get('old_value'),
                    "new_value": change.get('new_value')
                })
        
        # Items added
        if 'dictionary_item_added' in diff:
            for item in diff['dictionary_item_added']:
                differences.append({
                    "type": "item_added",
                    "path": str(item)
                })
        
        # Items removed
        if 'dictionary_item_removed' in diff:
            for item in diff['dictionary_item_removed']:
                differences.append({
                    "type": "item_removed",
                    "path": str(item)
                })
        
        # Type changes
        if 'type_changes' in diff:
            for path, change in diff['type_changes'].items():
                differences.append({
                    "type": "type_changed",
                    "path": path,
                    "old_type": str(change.get('old_type')),
                    "new_type": str(change.get('new_type'))
                })
        
        # Iterable items added
        if 'iterable_item_added' in diff:
            for path, value in diff['iterable_item_added'].items():
                differences.append({
                    "type": "item_added",
                    "path": path,
                    "value": value
                })
        
        # Iterable items removed
        if 'iterable_item_removed' in diff:
            for path, value in diff['iterable_item_removed'].items():
                differences.append({
                    "type": "item_removed",
                    "path": path,
                    "value": value
                })
        
        return differences
    
    def _generate_summary(self, diff: DeepDiff) -> Dict[str, int]:
        """Generate summary statistics of differences"""
        summary = {
            "total_differences": 0,
            "values_changed": 0,
            "items_added": 0,
            "items_removed": 0,
            "type_changes": 0
        }
        
        if 'values_changed' in diff:
            count = len(diff['values_changed'])
            summary['values_changed'] = count
            summary['total_differences'] += count
        
        if 'dictionary_item_added' in diff:
            count = len(diff['dictionary_item_added'])
            summary['items_added'] += count
            summary['total_differences'] += count
        
        if 'dictionary_item_removed' in diff:
            count = len(diff['dictionary_item_removed'])
            summary['items_removed'] += count
            summary['total_differences'] += count
        
        if 'type_changes' in diff:
            count = len(diff['type_changes'])
            summary['type_changes'] = count
            summary['total_differences'] += count
        
        if 'iterable_item_added' in diff:
            count = len(diff['iterable_item_added'])
            summary['items_added'] += count
            summary['total_differences'] += count
        
        if 'iterable_item_removed' in diff:
            count = len(diff['iterable_item_removed'])
            summary['items_removed'] += count
            summary['total_differences'] += count
        
        return summary
    
    def find_missing_keys(
        self,
        json1: str,
        json2: str
    ) -> Dict[str, List[str]]:
        """
        Find keys present in one JSON but missing in the other
        
        Args:
            json1: First JSON string
            json2: Second JSON string
            
        Returns:
            Dictionary with missing keys in each document
        """
        try:
            data1 = json.loads(json1)
            data2 = json.loads(json2)
            
            keys1 = self._get_all_keys(data1)
            keys2 = self._get_all_keys(data2)
            
            return {
                "missing_in_json2": sorted(list(keys1 - keys2)),
                "missing_in_json1": sorted(list(keys2 - keys1)),
                "common_keys": sorted(list(keys1 & keys2))
            }
            
        except Exception as e:
            raise ProcessingError(f"Key comparison failed: {str(e)}")
    
    def _get_all_keys(self, data: Any, prefix: str = "") -> set:
        """Get all keys in JSON structure"""
        keys = set()
        
        if isinstance(data, dict):
            for key, value in data.items():
                full_key = f"{prefix}.{key}" if prefix else key
                keys.add(full_key)
                keys.update(self._get_all_keys(value, full_key))
        
        elif isinstance(data, list):
            for idx, item in enumerate(data):
                keys.update(self._get_all_keys(item, f"{prefix}[{idx}]"))
        
        return keys
    
    def generate_patch(
        self,
        json1: str,
        json2: str
    ) -> List[Dict[str, Any]]:
        """
        Generate JSON patch (RFC 6902) to transform json1 to json2
        
        Args:
            json1: Source JSON string
            json2: Target JSON string
            
        Returns:
            List of patch operations
        """
        try:
            data1 = json.loads(json1)
            data2 = json.loads(json2)
            
            diff = DeepDiff(data1, data2, verbose_level=2)
            patch = []
            
            # Add operations for added items
            if 'dictionary_item_added' in diff:
                for item in diff['dictionary_item_added']:
                    path = str(item).replace("root", "")
                    patch.append({
                        "op": "add",
                        "path": path,
                        "value": None  # Would need to extract actual value
                    })
            
            # Remove operations for removed items
            if 'dictionary_item_removed' in diff:
                for item in diff['dictionary_item_removed']:
                    path = str(item).replace("root", "")
                    patch.append({
                        "op": "remove",
                        "path": path
                    })
            
            # Replace operations for changed values
            if 'values_changed' in diff:
                for path, change in diff['values_changed'].items():
                    json_path = path.replace("root", "")
                    patch.append({
                        "op": "replace",
                        "path": json_path,
                        "value": change.get('new_value')
                    })
            
            self.logger.info(f"Generated patch with {len(patch)} operations")
            return patch
            
        except Exception as e:
            raise ProcessingError(f"Patch generation failed: {str(e)}")


# Made with Bob