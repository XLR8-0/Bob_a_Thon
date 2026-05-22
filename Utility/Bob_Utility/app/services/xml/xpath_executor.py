"""
XPath Executor Service
Executes XPath queries on XML documents and generates XPath expressions
"""

from typing import List, Dict, Any, Optional, Tuple
from lxml import etree
from app.services.base import BaseService
from app.core.exceptions import ValidationError, ProcessingError


class XPathExecutor(BaseService):
    """Service for executing XPath queries and generating XPath expressions"""
    
    def __init__(self):
        super().__init__()
        self.logger.info("Initialized XPathExecutor")
    
    def execute_xpath(
        self,
        xml_content: str,
        xpath_query: str,
        namespaces: Optional[Dict[str, str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Execute XPath query on XML content
        
        Args:
            xml_content: XML string to query
            xpath_query: XPath expression to execute
            namespaces: Optional namespace mappings
            
        Returns:
            List of matching elements with their details
            
        Raises:
            ValidationError: If XML or XPath is invalid
            ProcessingError: If execution fails
        """
        try:
            # Parse XML
            try:
                root = etree.fromstring(xml_content.encode('utf-8'))
            except etree.XMLSyntaxError as e:
                raise ValidationError(f"Invalid XML: {str(e)}")
            
            # Execute XPath
            try:
                results = root.xpath(xpath_query, namespaces=namespaces or {})
            except etree.XPathEvalError as e:
                raise ValidationError(f"Invalid XPath expression: {str(e)}")
            
            # Process results
            matches = []
            for idx, result in enumerate(results):
                match_info = {
                    "index": idx,
                    "type": self._get_result_type(result),
                }
                
                if isinstance(result, etree._Element):
                    match_info.update({
                        "tag": result.tag,
                        "text": result.text,
                        "attributes": dict(result.attrib),
                        "xpath": self.generate_xpath(result),
                        "xml": etree.tostring(result, encoding='unicode', pretty_print=True)
                    })
                elif isinstance(result, str):
                    match_info["value"] = result
                elif isinstance(result, (int, float, bool)):
                    match_info["value"] = result
                else:
                    match_info["value"] = str(result)
                
                matches.append(match_info)
            
            self.logger.info(f"XPath query returned {len(matches)} results")
            return matches
            
        except ValidationError:
            raise
        except Exception as e:
            self.logger.error(f"XPath execution failed: {str(e)}")
            raise ProcessingError(f"Failed to execute XPath: {str(e)}")
    
    def generate_xpath(
        self,
        element: etree._Element,
        use_position: bool = True,
        use_attributes: bool = False
    ) -> str:
        """
        Generate XPath expression for an element
        
        Args:
            element: Element to generate XPath for
            use_position: Include position predicates
            use_attributes: Use attribute predicates when available
            
        Returns:
            XPath expression as string
        """
        try:
            path_parts = []
            current = element
            
            while current is not None:
                tag = current.tag
                
                # Handle namespace
                if '}' in tag:
                    tag = tag.split('}')[1]
                
                # Build predicate
                predicate = ""
                if use_attributes and current.attrib:
                    # Use first attribute for predicate
                    attr_name, attr_value = list(current.attrib.items())[0]
                    predicate = f"[@{attr_name}='{attr_value}']"
                elif use_position and current.getparent() is not None:
                    # Calculate position among siblings with same tag
                    siblings = [e for e in current.getparent() if e.tag == current.tag]
                    if len(siblings) > 1:
                        position = siblings.index(current) + 1
                        predicate = f"[{position}]"
                
                path_parts.insert(0, f"{tag}{predicate}")
                current = current.getparent()
            
            xpath = "/" + "/".join(path_parts)
            self.logger.debug(f"Generated XPath: {xpath}")
            return xpath
            
        except Exception as e:
            self.logger.error(f"XPath generation failed: {str(e)}")
            return "/error"
    
    def generate_xpath_local_name(
        self,
        element: etree._Element,
        include_text: bool = False
    ) -> str:
        """
        Generate namespace-agnostic XPath using local-name()
        
        Args:
            element: Element to generate XPath for
            include_text: Whether to append /text() at the end
            
        Returns:
            XPath expression using local-name() syntax
        """
        try:
            path_parts = []
            current = element
            
            while current is not None:
                tag = current.tag
                
                # Handle namespace - extract local name
                if '}' in tag:
                    tag = tag.split('}')[1]
                
                # Use local-name() for namespace-agnostic matching
                path_parts.insert(0, f"*[local-name()='{tag}']")
                current = current.getparent()
            
            xpath = "//" + "/".join(path_parts)
            if include_text:
                xpath += "/text()"
            
            self.logger.debug(f"Generated local-name XPath: {xpath}")
            return xpath
            
        except Exception as e:
            self.logger.error(f"Local-name XPath generation failed: {str(e)}")
            return "/error"
    
    def find_elements_by_text(
        self,
        xml_content: str,
        search_text: str,
        case_sensitive: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Find elements containing specific text
        
        Args:
            xml_content: XML string to search
            search_text: Text to search for
            case_sensitive: Whether search is case-sensitive
            
        Returns:
            List of matching elements with XPath
        """
        try:
            root = etree.fromstring(xml_content.encode('utf-8'))
            
            if case_sensitive:
                xpath = f"//*[contains(text(), '{search_text}')]"
            else:
                xpath = f"//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{search_text.lower()}')]"
            
            return self.execute_xpath(xml_content, xpath)
            
        except Exception as e:
            self.logger.error(f"Text search failed: {str(e)}")
            raise ProcessingError(f"Failed to search text: {str(e)}")
    
    def find_elements_by_attribute(
        self,
        xml_content: str,
        attribute_name: str,
        attribute_value: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Find elements by attribute name or name/value pair
        
        Args:
            xml_content: XML string to search
            attribute_name: Attribute name to search for
            attribute_value: Optional attribute value to match
            
        Returns:
            List of matching elements with XPath
        """
        try:
            if attribute_value:
                xpath = f"//*[@{attribute_name}='{attribute_value}']"
            else:
                xpath = f"//*[@{attribute_name}]"
            
            return self.execute_xpath(xml_content, xpath)
            
        except Exception as e:
            self.logger.error(f"Attribute search failed: {str(e)}")
            raise ProcessingError(f"Failed to search attribute: {str(e)}")
    
    def find_by_value(
        self,
        xml_content: str,
        search_value: str,
        case_sensitive: bool = False,
        exact_match: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Find elements by their text value and return their XPath expressions
        
        Args:
            xml_content: XML string to search
            search_value: Value to search for
            case_sensitive: Whether search is case-sensitive
            exact_match: Whether to match exact value or use contains
            
        Returns:
            List of matching elements with their XPath expressions
        """
        try:
            root = etree.fromstring(xml_content.encode('utf-8'))
            matches = []
            
            # Search for elements with matching text
            if exact_match:
                if case_sensitive:
                    xpath = f"//*[text()='{search_value}']"
                else:
                    xpath = f"//*[translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz')='{search_value.lower()}']"
            else:
                if case_sensitive:
                    xpath = f"//*[contains(text(), '{search_value}')]"
                else:
                    xpath = f"//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{search_value.lower()}')]"
            
            elements = root.xpath(xpath)
            
            for idx, element in enumerate(elements):
                generated_xpath = self.generate_xpath(element, use_position=True, use_attributes=False)
                local_name_xpath = self.generate_xpath_local_name(element, include_text=True)
                matches.append({
                    "index": idx,
                    "tag": element.tag.split('}')[1] if '}' in element.tag else element.tag,
                    "text": element.text,
                    "xpath": generated_xpath,
                    "xpath_local_name": local_name_xpath,
                    "attributes": dict(element.attrib),
                    "xml": etree.tostring(element, encoding='unicode', pretty_print=True)
                })
            
            self.logger.info(f"Found {len(matches)} elements with value '{search_value}'")
            return matches
            
        except Exception as e:
            self.logger.error(f"Value search failed: {str(e)}")
            raise ProcessingError(f"Failed to search by value: {str(e)}")
    
    def validate_xpath(self, xpath_query: str) -> Tuple[bool, Optional[str]]:
        """
        Validate XPath expression syntax
        
        Args:
            xpath_query: XPath expression to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            # Try to compile the XPath
            etree.XPath(xpath_query)
            return True, None
        except etree.XPathSyntaxError as e:
            return False, str(e)
        except Exception as e:
            return False, f"Unexpected error: {str(e)}"
    
    def get_xpath_suggestions(
        self,
        xml_content: str,
        partial_xpath: str = ""
    ) -> List[str]:
        """
        Get XPath suggestions based on XML structure
        
        Args:
            xml_content: XML string to analyze
            partial_xpath: Partial XPath to complete
            
        Returns:
            List of suggested XPath expressions
        """
        try:
            root = etree.fromstring(xml_content.encode('utf-8'))
            suggestions = []
            
            # Get all unique tag names
            tags = set()
            for elem in root.iter():
                tag = elem.tag
                if '}' in tag:
                    tag = tag.split('}')[1]
                tags.add(tag)
            
            # Generate basic suggestions
            for tag in sorted(tags):
                suggestions.append(f"//{tag}")
                suggestions.append(f"//{tag}[@*]")  # Elements with any attribute
                suggestions.append(f"//{tag}[text()]")  # Elements with text
            
            return suggestions[:20]  # Limit to 20 suggestions
            
        except Exception as e:
            self.logger.error(f"Failed to generate suggestions: {str(e)}")
            return []
    
    def _get_result_type(self, result: Any) -> str:
        """Get the type of XPath result"""
        if isinstance(result, etree._Element):
            return "element"
        elif isinstance(result, str):
            return "string"
        elif isinstance(result, bool):
            return "boolean"
        elif isinstance(result, (int, float)):
            return "number"
        else:
            return "unknown"


# Made with Bob