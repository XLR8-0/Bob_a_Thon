"""
XML Tree Explorer Service
Provides tree structure visualization and navigation for XML documents
"""

from typing import List, Dict, Any, Optional
from lxml import etree
from app.services.base import BaseService
from app.core.exceptions import ValidationError, ProcessingError


class XMLTreeExplorer(BaseService):
    """Service for exploring XML document tree structure"""
    
    def __init__(self):
        super().__init__()
        self.logger.info("Initialized XMLTreeExplorer")
    
    def get_tree_structure(
        self,
        xml_content: str,
        max_depth: Optional[int] = None,
        include_attributes: bool = True,
        include_text: bool = True
    ) -> Dict[str, Any]:
        """
        Get hierarchical tree structure of XML document
        
        Args:
            xml_content: XML string to analyze
            max_depth: Maximum depth to traverse (None for unlimited)
            include_attributes: Include element attributes
            include_text: Include element text content
            
        Returns:
            Tree structure as nested dictionary
            
        Raises:
            ValidationError: If XML is invalid
            ProcessingError: If tree generation fails
        """
        try:
            # Parse XML
            try:
                root = etree.fromstring(xml_content.encode('utf-8'))
            except etree.XMLSyntaxError as e:
                raise ValidationError(f"Invalid XML: {str(e)}")
            
            # Build tree structure
            tree = self._build_tree_node(
                root,
                depth=0,
                max_depth=max_depth,
                include_attributes=include_attributes,
                include_text=include_text
            )
            
            self.logger.info("Successfully generated tree structure")
            return tree
            
        except ValidationError:
            raise
        except Exception as e:
            self.logger.error(f"Tree generation failed: {str(e)}")
            raise ProcessingError(f"Failed to generate tree: {str(e)}")
    
    def _build_tree_node(
        self,
        element: etree._Element,
        depth: int,
        max_depth: Optional[int],
        include_attributes: bool,
        include_text: bool,
        parent_path: str = ""
    ) -> Dict[str, Any]:
        """Build tree node for an element"""
        
        # Check depth limit
        if max_depth is not None and depth > max_depth:
            return {"truncated": True}
        
        # Get tag name (remove namespace if present)
        tag = element.tag
        if '}' in tag:
            namespace, tag = tag.split('}')
            namespace = namespace[1:]  # Remove leading {
        else:
            namespace = None
        
        # Build node path
        node_path = f"{parent_path}/{tag}" if parent_path else f"/{tag}"
        
        # Build node info
        node = {
            "tag": tag,
            "path": node_path,
            "depth": depth,
            "has_children": len(element) > 0,
            "child_count": len(element)
        }
        
        # Add namespace if present
        if namespace:
            node["namespace"] = namespace
        
        # Add attributes
        if include_attributes and element.attrib:
            node["attributes"] = dict(element.attrib)
            node["attribute_count"] = len(element.attrib)
        
        # Add text content
        if include_text:
            text = element.text.strip() if element.text else ""
            if text:
                node["text"] = text
                node["text_length"] = len(text)
        
        # Add children recursively
        if len(element) > 0:
            children = []
            for child in element:
                child_node = self._build_tree_node(
                    child,
                    depth + 1,
                    max_depth,
                    include_attributes,
                    include_text,
                    node_path
                )
                children.append(child_node)
            node["children"] = children
        
        return node
    
    def get_statistics(self, xml_content: str) -> Dict[str, Any]:
        """
        Get statistics about XML document structure
        
        Args:
            xml_content: XML string to analyze
            
        Returns:
            Dictionary with statistics
        """
        try:
            root = etree.fromstring(xml_content.encode('utf-8'))
            
            stats = {
                "total_elements": 0,
                "max_depth": 0,
                "total_attributes": 0,
                "total_text_nodes": 0,
                "unique_tags": set(),
                "unique_attributes": set(),
                "namespaces": set()
            }
            
            def traverse(element: etree._Element, depth: int):
                stats["total_elements"] += 1
                stats["max_depth"] = max(stats["max_depth"], depth)
                
                # Track tag
                tag = element.tag
                if '}' in tag:
                    namespace, tag = tag.split('}')
                    stats["namespaces"].add(namespace[1:])
                stats["unique_tags"].add(tag)
                
                # Track attributes
                if element.attrib:
                    stats["total_attributes"] += len(element.attrib)
                    stats["unique_attributes"].update(element.attrib.keys())
                
                # Track text
                if element.text and element.text.strip():
                    stats["total_text_nodes"] += 1
                
                # Recurse
                for child in element:
                    traverse(child, depth + 1)
            
            traverse(root, 0)
            
            # Convert sets to lists for JSON serialization
            stats["unique_tags"] = sorted(list(stats["unique_tags"]))
            stats["unique_attributes"] = sorted(list(stats["unique_attributes"]))
            stats["namespaces"] = sorted(list(stats["namespaces"]))
            stats["unique_tag_count"] = len(stats["unique_tags"])
            stats["unique_attribute_count"] = len(stats["unique_attributes"])
            
            self.logger.info(f"Generated statistics: {stats['total_elements']} elements")
            return stats
            
        except Exception as e:
            self.logger.error(f"Statistics generation failed: {str(e)}")
            raise ProcessingError(f"Failed to generate statistics: {str(e)}")
    
    def find_node_by_path(
        self,
        xml_content: str,
        path: str
    ) -> Optional[Dict[str, Any]]:
        """
        Find a specific node by its path
        
        Args:
            xml_content: XML string to search
            path: Node path (e.g., "/root/child/grandchild")
            
        Returns:
            Node information or None if not found
        """
        try:
            root = etree.fromstring(xml_content.encode('utf-8'))
            
            # Split path and navigate
            parts = [p for p in path.split('/') if p]
            current = root
            
            for part in parts[1:]:  # Skip root
                found = False
                for child in current:
                    tag = child.tag
                    if '}' in tag:
                        tag = tag.split('}')[1]
                    if tag == part:
                        current = child
                        found = True
                        break
                if not found:
                    return None
            
            # Build node info
            return self._build_tree_node(current, 0, 2, True, True)
            
        except Exception as e:
            self.logger.error(f"Node search failed: {str(e)}")
            return None
    
    def get_siblings(
        self,
        xml_content: str,
        element_path: str
    ) -> List[Dict[str, Any]]:
        """
        Get sibling elements of a specific element
        
        Args:
            xml_content: XML string
            element_path: Path to the element
            
        Returns:
            List of sibling elements
        """
        try:
            root = etree.fromstring(xml_content.encode('utf-8'))
            
            # Find the element
            parts = [p for p in element_path.split('/') if p]
            current = root
            
            for part in parts[1:]:
                for child in current:
                    tag = child.tag
                    if '}' in tag:
                        tag = tag.split('}')[1]
                    if tag == part:
                        current = child
                        break
            
            # Get parent and siblings
            parent = current.getparent()
            if parent is None:
                return []
            
            siblings = []
            for sibling in parent:
                if sibling != current:
                    node = self._build_tree_node(sibling, 0, 1, True, True)
                    siblings.append(node)
            
            return siblings
            
        except Exception as e:
            self.logger.error(f"Sibling search failed: {str(e)}")
            return []
    
    def get_ancestors(
        self,
        xml_content: str,
        element_path: str
    ) -> List[Dict[str, Any]]:
        """
        Get ancestor elements of a specific element
        
        Args:
            xml_content: XML string
            element_path: Path to the element
            
        Returns:
            List of ancestor elements (from root to parent)
        """
        try:
            root = etree.fromstring(xml_content.encode('utf-8'))
            
            # Find the element
            parts = [p for p in element_path.split('/') if p]
            current = root
            ancestors = [self._build_tree_node(root, 0, 0, True, False)]
            
            for part in parts[1:]:
                for child in current:
                    tag = child.tag
                    if '}' in tag:
                        tag = tag.split('}')[1]
                    if tag == part:
                        current = child
                        ancestors.append(self._build_tree_node(current, 0, 0, True, False))
                        break
            
            return ancestors[:-1]  # Exclude the element itself
            
        except Exception as e:
            self.logger.error(f"Ancestor search failed: {str(e)}")
            return []


# Made with Bob