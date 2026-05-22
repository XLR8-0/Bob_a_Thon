"""
XSD Validator Service
Validates XML documents against XSD schemas
"""

from typing import List, Dict, Any, Optional, Tuple
from lxml import etree
from app.services.base import BaseService
from app.core.exceptions import ValidationError, ProcessingError


class XSDValidator(BaseService):
    """Service for validating XML against XSD schemas"""
    
    def __init__(self):
        super().__init__()
        self.logger.info("Initialized XSDValidator")
        self._schema_cache = {}
    
    def validate_against_xsd(
        self,
        xml_content: str,
        xsd_content: str,
        cache_schema: bool = True
    ) -> Dict[str, Any]:
        """
        Validate XML against XSD schema
        
        Args:
            xml_content: XML string to validate
            xsd_content: XSD schema string
            cache_schema: Whether to cache the compiled schema
            
        Returns:
            Dictionary with validation results
            
        Raises:
            ValidationError: If XML or XSD is invalid
            ProcessingError: If validation fails
        """
        try:
            # Parse XML
            try:
                xml_doc = etree.fromstring(xml_content.encode('utf-8'))
            except etree.XMLSyntaxError as e:
                raise ValidationError(f"Invalid XML: {str(e)}")
            
            # Get or compile schema
            schema_hash = hash(xsd_content)
            if cache_schema and schema_hash in self._schema_cache:
                schema = self._schema_cache[schema_hash]
                self.logger.debug("Using cached schema")
            else:
                try:
                    xsd_doc = etree.fromstring(xsd_content.encode('utf-8'))
                    schema = etree.XMLSchema(xsd_doc)
                    if cache_schema:
                        self._schema_cache[schema_hash] = schema
                        self.logger.debug("Schema compiled and cached")
                except etree.XMLSchemaParseError as e:
                    raise ValidationError(f"Invalid XSD schema: {str(e)}")
            
            # Validate
            is_valid = schema.validate(xml_doc)
            errors = []
            
            if not is_valid:
                for error in schema.error_log:
                    errors.append({
                        "line": error.line,
                        "column": error.column,
                        "message": error.message,
                        "level": error.level_name,
                        "type": error.type_name,
                        "domain": error.domain_name
                    })
            
            result = {
                "valid": is_valid,
                "error_count": len(errors),
                "errors": errors
            }
            
            self.logger.info(f"Validation complete: {'valid' if is_valid else 'invalid'}")
            return result
            
        except ValidationError:
            raise
        except Exception as e:
            self.logger.error(f"XSD validation failed: {str(e)}")
            raise ProcessingError(f"Failed to validate XML: {str(e)}")
    
    def validate_well_formed(self, xml_content: str) -> Dict[str, Any]:
        """
        Check if XML is well-formed (basic syntax validation)
        
        Args:
            xml_content: XML string to validate
            
        Returns:
            Dictionary with validation results
        """
        try:
            try:
                etree.fromstring(xml_content.encode('utf-8'))
                return {
                    "valid": True,
                    "error_count": 0,
                    "errors": []
                }
            except etree.XMLSyntaxError as e:
                return {
                    "valid": False,
                    "error_count": 1,
                    "errors": [{
                        "line": e.lineno,
                        "column": e.offset,
                        "message": str(e),
                        "level": "ERROR",
                        "type": "XMLSyntaxError"
                    }]
                }
        except Exception as e:
            self.logger.error(f"Well-formed check failed: {str(e)}")
            raise ProcessingError(f"Failed to check XML: {str(e)}")
    
    def validate_against_dtd(
        self,
        xml_content: str,
        dtd_content: str
    ) -> Dict[str, Any]:
        """
        Validate XML against DTD
        
        Args:
            xml_content: XML string to validate
            dtd_content: DTD string
            
        Returns:
            Dictionary with validation results
        """
        try:
            # Parse XML
            try:
                xml_doc = etree.fromstring(xml_content.encode('utf-8'))
            except etree.XMLSyntaxError as e:
                raise ValidationError(f"Invalid XML: {str(e)}")
            
            # Parse DTD
            try:
                dtd = etree.DTD(etree.fromstring(f"<!DOCTYPE root [{dtd_content}]><root/>".encode('utf-8')))
            except Exception as e:
                raise ValidationError(f"Invalid DTD: {str(e)}")
            
            # Validate
            is_valid = dtd.validate(xml_doc)
            errors = []
            
            if not is_valid:
                for error in dtd.error_log:
                    errors.append({
                        "line": error.line,
                        "column": error.column,
                        "message": error.message,
                        "level": error.level_name,
                        "type": error.type_name
                    })
            
            return {
                "valid": is_valid,
                "error_count": len(errors),
                "errors": errors
            }
            
        except ValidationError:
            raise
        except Exception as e:
            self.logger.error(f"DTD validation failed: {str(e)}")
            raise ProcessingError(f"Failed to validate against DTD: {str(e)}")
    
    def generate_xsd_from_xml(
        self,
        xml_content: str,
        target_namespace: Optional[str] = None
    ) -> str:
        """
        Generate a basic XSD schema from XML structure
        
        Args:
            xml_content: XML string to analyze
            target_namespace: Optional target namespace for schema
            
        Returns:
            Generated XSD schema as string
        """
        try:
            root = etree.fromstring(xml_content.encode('utf-8'))
            
            # Build schema structure
            schema_root = etree.Element(
                "{http://www.w3.org/2001/XMLSchema}schema",
                nsmap={'xs': 'http://www.w3.org/2001/XMLSchema'}
            )
            
            if target_namespace:
                schema_root.set('targetNamespace', target_namespace)
                schema_root.set('xmlns', target_namespace)
            
            # Generate element definitions
            self._generate_element_definition(root, schema_root)
            
            xsd = etree.tostring(
                schema_root,
                encoding='unicode',
                pretty_print=True,
                xml_declaration=True
            )
            
            self.logger.info("Generated XSD schema from XML")
            return xsd
            
        except Exception as e:
            self.logger.error(f"XSD generation failed: {str(e)}")
            raise ProcessingError(f"Failed to generate XSD: {str(e)}")
    
    def _generate_element_definition(
        self,
        element: etree._Element,
        schema_root: etree._Element,
        processed: Optional[set] = None
    ):
        """Generate XSD element definition recursively"""
        if processed is None:
            processed = set()
        
        tag = element.tag
        if '}' in tag:
            tag = tag.split('}')[1]
        
        if tag in processed:
            return
        processed.add(tag)
        
        # Create element definition
        xs_element = etree.SubElement(
            schema_root,
            "{http://www.w3.org/2001/XMLSchema}element"
        )
        xs_element.set('name', tag)
        
        # Create complex type if element has children or attributes
        if len(element) > 0 or element.attrib:
            xs_complex = etree.SubElement(
                xs_element,
                "{http://www.w3.org/2001/XMLSchema}complexType"
            )
            
            # Add sequence for children
            if len(element) > 0:
                xs_sequence = etree.SubElement(
                    xs_complex,
                    "{http://www.w3.org/2001/XMLSchema}sequence"
                )
                
                # Add child elements
                for child in element:
                    child_tag = child.tag
                    if '}' in child_tag:
                        child_tag = child_tag.split('}')[1]
                    
                    xs_child = etree.SubElement(
                        xs_sequence,
                        "{http://www.w3.org/2001/XMLSchema}element"
                    )
                    xs_child.set('ref', child_tag)
                    xs_child.set('minOccurs', '0')
                    xs_child.set('maxOccurs', 'unbounded')
                    
                    # Recursively process child
                    self._generate_element_definition(child, schema_root, processed)
            
            # Add attributes
            for attr_name in element.attrib:
                xs_attr = etree.SubElement(
                    xs_complex,
                    "{http://www.w3.org/2001/XMLSchema}attribute"
                )
                xs_attr.set('name', attr_name)
                xs_attr.set('type', 'xs:string')
        else:
            # Simple type
            xs_element.set('type', 'xs:string')
    
    def get_schema_info(self, xsd_content: str) -> Dict[str, Any]:
        """
        Extract information from XSD schema
        
        Args:
            xsd_content: XSD schema string
            
        Returns:
            Dictionary with schema information
        """
        try:
            xsd_doc = etree.fromstring(xsd_content.encode('utf-8'))
            
            info = {
                "target_namespace": xsd_doc.get('targetNamespace'),
                "elements": [],
                "complex_types": [],
                "simple_types": [],
                "attributes": []
            }
            
            # Find all elements
            for elem in xsd_doc.findall('.//{http://www.w3.org/2001/XMLSchema}element'):
                name = elem.get('name')
                if name:
                    info['elements'].append({
                        "name": name,
                        "type": elem.get('type'),
                        "min_occurs": elem.get('minOccurs', '1'),
                        "max_occurs": elem.get('maxOccurs', '1')
                    })
            
            # Find all complex types
            for ctype in xsd_doc.findall('.//{http://www.w3.org/2001/XMLSchema}complexType'):
                name = ctype.get('name')
                if name:
                    info['complex_types'].append(name)
            
            # Find all simple types
            for stype in xsd_doc.findall('.//{http://www.w3.org/2001/XMLSchema}simpleType'):
                name = stype.get('name')
                if name:
                    info['simple_types'].append(name)
            
            # Find all attributes
            for attr in xsd_doc.findall('.//{http://www.w3.org/2001/XMLSchema}attribute'):
                name = attr.get('name')
                if name:
                    info['attributes'].append({
                        "name": name,
                        "type": attr.get('type'),
                        "use": attr.get('use', 'optional')
                    })
            
            return info
            
        except Exception as e:
            self.logger.error(f"Schema info extraction failed: {str(e)}")
            raise ProcessingError(f"Failed to extract schema info: {str(e)}")
    
    def clear_cache(self):
        """Clear the schema cache"""
        self._schema_cache.clear()
        self.logger.info("Schema cache cleared")


# Made with Bob