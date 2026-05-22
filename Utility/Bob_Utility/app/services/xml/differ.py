"""
XML Differ Service
Compares two XML documents and identifies differences
"""

from typing import List, Dict, Any, Optional
from lxml import etree
from deepdiff import DeepDiff
import xmltodict
from app.services.base import BaseService
from app.core.exceptions import ValidationError, ProcessingError


class XMLDiffer(BaseService):
    """Service for comparing XML documents"""
    
    def __init__(self):
        super().__init__()
        self.logger.info("Initialized XMLDiffer")
    
    def compare_xml(
        self,
        xml1: str,
        xml2: str,
        ignore_order: bool = False,
        ignore_whitespace: bool = True,
        ignore_comments: bool = True,
        ignore_attributes: bool = False
    ) -> Dict[str, Any]:
        """
        Compare two XML documents
        
        Args:
            xml1: First XML string
            xml2: Second XML string
            ignore_order: Ignore element order
            ignore_whitespace: Ignore whitespace differences
            ignore_comments: Ignore XML comments
            ignore_attributes: Ignore attribute differences
            
        Returns:
            Dictionary with comparison results
            
        Raises:
            ValidationError: If XML is invalid
            ProcessingError: If comparison fails
        """
        try:
            # Parse both XML documents
            try:
                root1 = etree.fromstring(xml1.encode('utf-8'))
                root2 = etree.fromstring(xml2.encode('utf-8'))
            except etree.XMLSyntaxError as e:
                raise ValidationError(f"Invalid XML: {str(e)}")
            
            # Remove comments if requested
            if ignore_comments:
                etree.strip_tags(root1, etree.Comment)
                etree.strip_tags(root2, etree.Comment)
            
            # Convert to dictionaries for deep comparison
            dict1 = xmltodict.parse(etree.tostring(root1))
            dict2 = xmltodict.parse(etree.tostring(root2))
            
            # Perform deep comparison
            diff = DeepDiff(
                dict1,
                dict2,
                ignore_order=ignore_order,
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
            self.logger.error(f"XML comparison failed: {str(e)}")
            raise ProcessingError(f"Failed to compare XML: {str(e)}")
    
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
                    "path": str(item),
                    "value": None
                })
        
        # Items removed
        if 'dictionary_item_removed' in diff:
            for item in diff['dictionary_item_removed']:
                differences.append({
                    "type": "item_removed",
                    "path": str(item),
                    "value": None
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
    
    def compare_structure(
        self,
        xml1: str,
        xml2: str
    ) -> Dict[str, Any]:
        """
        Compare only the structure (tags and hierarchy) of two XML documents
        
        Args:
            xml1: First XML string
            xml2: Second XML string
            
        Returns:
            Dictionary with structure comparison results
        """
        try:
            root1 = etree.fromstring(xml1.encode('utf-8'))
            root2 = etree.fromstring(xml2.encode('utf-8'))
            
            structure1 = self._extract_structure(root1)
            structure2 = self._extract_structure(root2)
            
            diff = DeepDiff(structure1, structure2, ignore_order=False)
            
            return {
                "identical": len(diff) == 0,
                "differences": self._process_differences(diff),
                "summary": self._generate_summary(diff)
            }
            
        except Exception as e:
            self.logger.error(f"Structure comparison failed: {str(e)}")
            raise ProcessingError(f"Failed to compare structure: {str(e)}")
    
    def _extract_structure(self, element: etree._Element, path: str = "") -> Dict[str, Any]:
        """Extract structure (tags only) from XML element"""
        tag = element.tag
        if '}' in tag:
            tag = tag.split('}')[1]
        
        current_path = f"{path}/{tag}" if path else f"/{tag}"
        
        structure = {
            "tag": tag,
            "path": current_path,
            "children": []
        }
        
        for child in element:
            structure["children"].append(
                self._extract_structure(child, current_path)
            )
        
        return structure
    
    def find_missing_elements(
        self,
        xml1: str,
        xml2: str
    ) -> Dict[str, List[str]]:
        """
        Find elements present in one XML but missing in the other
        
        Args:
            xml1: First XML string
            xml2: Second XML string
            
        Returns:
            Dictionary with missing elements in each document
        """
        try:
            root1 = etree.fromstring(xml1.encode('utf-8'))
            root2 = etree.fromstring(xml2.encode('utf-8'))
            
            paths1 = self._get_all_paths(root1)
            paths2 = self._get_all_paths(root2)
            
            return {
                "missing_in_xml2": sorted(list(paths1 - paths2)),
                "missing_in_xml1": sorted(list(paths2 - paths1)),
                "common_paths": sorted(list(paths1 & paths2))
            }
            
        except Exception as e:
            self.logger.error(f"Missing elements search failed: {str(e)}")
            raise ProcessingError(f"Failed to find missing elements: {str(e)}")
    
    def _get_all_paths(self, element: etree._Element, path: str = "") -> set:
        """Get all element paths in XML tree"""
        tag = element.tag
        if '}' in tag:
            tag = tag.split('}')[1]
        
        current_path = f"{path}/{tag}" if path else f"/{tag}"
        paths = {current_path}
        
        for child in element:
            paths.update(self._get_all_paths(child, current_path))
        
        return paths
    
    def generate_diff_report(
        self,
        xml1: str,
        xml2: str,
        format: str = "text"
    ) -> str:
        """
        Generate a human-readable diff report
        
        Args:
            xml1: First XML string
            xml2: Second XML string
            format: Output format ('text' or 'html')
            
        Returns:
            Formatted diff report
        """
        try:
            comparison = self.compare_xml(xml1, xml2)
            
            if format == "html":
                return self._generate_html_report(comparison)
            else:
                return self._generate_text_report(comparison)
                
        except Exception as e:
            self.logger.error(f"Report generation failed: {str(e)}")
            raise ProcessingError(f"Failed to generate report: {str(e)}")
    
    def _generate_text_report(self, comparison: Dict[str, Any]) -> str:
        """Generate text format diff report"""
        lines = ["XML Comparison Report", "=" * 50, ""]
        
        summary = comparison['summary']
        lines.append(f"Total Differences: {summary['total_differences']}")
        lines.append(f"Values Changed: {summary['values_changed']}")
        lines.append(f"Items Added: {summary['items_added']}")
        lines.append(f"Items Removed: {summary['items_removed']}")
        lines.append(f"Type Changes: {summary['type_changes']}")
        lines.append("")
        
        if comparison['differences']:
            lines.append("Detailed Differences:")
            lines.append("-" * 50)
            for diff in comparison['differences']:
                lines.append(f"\nType: {diff['type']}")
                lines.append(f"Path: {diff['path']}")
                if 'old_value' in diff:
                    lines.append(f"Old: {diff['old_value']}")
                if 'new_value' in diff:
                    lines.append(f"New: {diff['new_value']}")
        
        return "\n".join(lines)
    
    def _generate_html_report(self, comparison: Dict[str, Any]) -> str:
        """Generate HTML format diff report"""
        html = ["<html><body>"]
        html.append("<h1>XML Comparison Report</h1>")
        
        summary = comparison['summary']
        html.append("<h2>Summary</h2>")
        html.append("<ul>")
        html.append(f"<li>Total Differences: {summary['total_differences']}</li>")
        html.append(f"<li>Values Changed: {summary['values_changed']}</li>")
        html.append(f"<li>Items Added: {summary['items_added']}</li>")
        html.append(f"<li>Items Removed: {summary['items_removed']}</li>")
        html.append(f"<li>Type Changes: {summary['type_changes']}</li>")
        html.append("</ul>")
        
        if comparison['differences']:
            html.append("<h2>Detailed Differences</h2>")
            html.append("<table border='1'>")
            html.append("<tr><th>Type</th><th>Path</th><th>Details</th></tr>")
            for diff in comparison['differences']:
                html.append("<tr>")
                html.append(f"<td>{diff['type']}</td>")
                html.append(f"<td>{diff['path']}</td>")
                details = []
                if 'old_value' in diff:
                    details.append(f"Old: {diff['old_value']}")
                if 'new_value' in diff:
                    details.append(f"New: {diff['new_value']}")
                html.append(f"<td>{'<br>'.join(details)}</td>")
                html.append("</tr>")
            html.append("</table>")
        
        html.append("</body></html>")
        return "\n".join(html)


# Made with Bob