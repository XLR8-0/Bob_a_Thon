"""
XML Converter Service
Converts XML to/from other formats (JSON, YAML, Dict)
"""

from typing import Dict, Any, Optional
import json
import yaml
from lxml import etree  # type: ignore
import xmltodict
from app.services.base import BaseService
from app.core.exceptions import ValidationError, ProcessingError


class XMLConverter(BaseService):
    """Service for converting XML to other formats"""
    
    def __init__(self):
        super().__init__()
        self.logger.info("Initialized XMLConverter")
    
    def xml_to_json(
        self,
        xml_content: str,
        pretty: bool = True,
        indent: int = 2
    ) -> str:
        """
        Convert XML to JSON
        
        Args:
            xml_content: XML string to convert
            pretty: Whether to format JSON with indentation
            indent: Number of spaces for indentation
            
        Returns:
            JSON string
            
        Raises:
            ValidationError: If XML is invalid
            ProcessingError: If conversion fails
        """
        try:
            # Parse XML to dict
            data = xmltodict.parse(xml_content)
            
            # Convert to JSON
            if pretty:
                json_str = json.dumps(data, indent=indent, ensure_ascii=False)
            else:
                json_str = json.dumps(data, ensure_ascii=False)
            
            self.logger.info("Successfully converted XML to JSON")
            return json_str
            
        except Exception as e:
            self.logger.error(f"XML to JSON conversion failed: {str(e)}")
            raise ProcessingError(f"Failed to convert XML to JSON: {str(e)}")
    
    def xml_to_dict(self, xml_content: str) -> Dict[str, Any]:
        """
        Convert XML to Python dictionary
        
        Args:
            xml_content: XML string to convert
            
        Returns:
            Dictionary representation of XML
        """
        try:
            data = xmltodict.parse(xml_content)
            self.logger.info("Successfully converted XML to dict")
            return data
        except Exception as e:
            self.logger.error(f"XML to dict conversion failed: {str(e)}")
            raise ProcessingError(f"Failed to convert XML to dict: {str(e)}")
    
    def xml_to_yaml(
        self,
        xml_content: str,
        default_flow_style: bool = False
    ) -> str:
        """
        Convert XML to YAML
        
        Args:
            xml_content: XML string to convert
            default_flow_style: YAML flow style setting
            
        Returns:
            YAML string
        """
        try:
            # Convert XML to dict first
            data = xmltodict.parse(xml_content)
            
            # Convert dict to YAML
            yaml_str = yaml.dump(
                data,
                default_flow_style=default_flow_style,
                allow_unicode=True,
                sort_keys=False
            )
            
            self.logger.info("Successfully converted XML to YAML")
            return yaml_str
            
        except Exception as e:
            self.logger.error(f"XML to YAML conversion failed: {str(e)}")
            raise ProcessingError(f"Failed to convert XML to YAML: {str(e)}")
    
    def json_to_xml(
        self,
        json_content: str,
        root_tag: str = "root",
        pretty: bool = True,
        indent: int = 2
    ) -> str:
        """
        Convert JSON to XML
        
        Args:
            json_content: JSON string to convert
            root_tag: Root element tag name
            pretty: Whether to format XML with indentation
            indent: Number of spaces for indentation
            
        Returns:
            XML string
        """
        try:
            # Parse JSON
            try:
                data = json.loads(json_content)
            except json.JSONDecodeError as e:
                raise ValidationError(f"Invalid JSON: {str(e)}")
            
            # Handle arrays by wrapping each item in an 'item' tag
            if isinstance(data, list):
                # For arrays, we need to wrap items properly
                # Create a structure that xmltodict can handle
                items = []
                for item in data:
                    items.append(item)
                wrapped_data = {root_tag: {'item': items}}
            elif isinstance(data, dict):
                # If it's already a dict, just wrap it with root tag
                wrapped_data = {root_tag: data}
            else:
                # For primitive types, wrap in root tag
                wrapped_data = {root_tag: data}
            
            # Convert to XML with full_document=True to ensure single root
            xml_str = xmltodict.unparse(
                wrapped_data,
                pretty=pretty,
                indent=" " * indent,
                full_document=True
            )
            
            self.logger.info("Successfully converted JSON to XML")
            return xml_str
            
        except ValidationError:
            raise
        except Exception as e:
            self.logger.error(f"JSON to XML conversion failed: {str(e)}")
            raise ProcessingError(f"Failed to convert JSON to XML: {str(e)}")
    
    def dict_to_xml(
        self,
        data: Dict[str, Any],
        root_tag: str = "root",
        pretty: bool = True,
        indent: int = 2
    ) -> str:
        """
        Convert Python dictionary to XML
        
        Args:
            data: Dictionary to convert
            root_tag: Root element tag name
            pretty: Whether to format XML with indentation
            indent: Number of spaces for indentation
            
        Returns:
            XML string
        """
        try:
            xml_str = xmltodict.unparse(
                {root_tag: data},
                pretty=pretty,
                indent=" " * indent
            )
            
            self.logger.info("Successfully converted dict to XML")
            return xml_str
            
        except Exception as e:
            self.logger.error(f"Dict to XML conversion failed: {str(e)}")
            raise ProcessingError(f"Failed to convert dict to XML: {str(e)}")
    
    def yaml_to_xml(
        self,
        yaml_content: str,
        root_tag: str = "root",
        pretty: bool = True,
        indent: int = 2
    ) -> str:
        """
        Convert YAML to XML
        
        Args:
            yaml_content: YAML string to convert
            root_tag: Root element tag name
            pretty: Whether to format XML with indentation
            indent: Number of spaces for indentation
            
        Returns:
            XML string
        """
        try:
            # Parse YAML
            try:
                data = yaml.safe_load(yaml_content)
            except yaml.YAMLError as e:
                raise ValidationError(f"Invalid YAML: {str(e)}")
            
            # Convert to XML
            xml_str = xmltodict.unparse(
                {root_tag: data},
                pretty=pretty,
                indent=" " * indent
            )
            
            self.logger.info("Successfully converted YAML to XML")
            return xml_str
            
        except ValidationError:
            raise
        except Exception as e:
            self.logger.error(f"YAML to XML conversion failed: {str(e)}")
            raise ProcessingError(f"Failed to convert YAML to XML: {str(e)}")
    
    def xml_to_csv(
        self,
        xml_content: str,
        delimiter: str = ",",
        include_header: bool = True
    ) -> str:
        """
        Convert XML to CSV (for simple tabular XML structures)
        
        Args:
            xml_content: XML string to convert
            delimiter: CSV delimiter
            include_header: Whether to include header row
            
        Returns:
            CSV string
        """
        try:
            root = etree.fromstring(xml_content.encode('utf-8'))
            
            # Collect all unique field names
            fields = set()
            rows = []
            
            for child in root:
                row = {}
                for elem in child:
                    tag = elem.tag
                    if '}' in tag:
                        tag = tag.split('}')[1]
                    fields.add(tag)
                    row[tag] = elem.text or ""
                rows.append(row)
            
            fields = sorted(list(fields))
            
            # Build CSV
            csv_lines = []
            
            if include_header:
                csv_lines.append(delimiter.join(fields))
            
            for row in rows:
                values = [row.get(field, "") for field in fields]
                csv_lines.append(delimiter.join(f'"{v}"' for v in values))
            
            csv_str = "\n".join(csv_lines)
            self.logger.info("Successfully converted XML to CSV")
            return csv_str
            
        except Exception as e:
            self.logger.error(f"XML to CSV conversion failed: {str(e)}")
            raise ProcessingError(f"Failed to convert XML to CSV: {str(e)}")
    
    def xml_to_html_table(
        self,
        xml_content: str,
        table_class: str = "xml-table"
    ) -> str:
        """
        Convert XML to HTML table (for simple tabular XML structures)
        
        Args:
            xml_content: XML string to convert
            table_class: CSS class for table
            
        Returns:
            HTML table string
        """
        try:
            root = etree.fromstring(xml_content.encode('utf-8'))
            
            # Collect all unique field names
            fields = set()
            rows = []
            
            for child in root:
                row = {}
                for elem in child:
                    tag = elem.tag
                    if '}' in tag:
                        tag = tag.split('}')[1]
                    fields.add(tag)
                    row[tag] = elem.text or ""
                rows.append(row)
            
            fields = sorted(list(fields))
            
            # Build HTML table
            html = [f'<table class="{table_class}">']
            
            # Header
            html.append("<thead><tr>")
            for field in fields:
                html.append(f"<th>{field}</th>")
            html.append("</tr></thead>")
            
            # Body
            html.append("<tbody>")
            for row in rows:
                html.append("<tr>")
                for field in fields:
                    value = row.get(field, "")
                    html.append(f"<td>{value}</td>")
                html.append("</tr>")
            html.append("</tbody>")
            
            html.append("</table>")
            
            html_str = "\n".join(html)
            self.logger.info("Successfully converted XML to HTML table")
            return html_str
            
        except Exception as e:
            self.logger.error(f"XML to HTML conversion failed: {str(e)}")
            raise ProcessingError(f"Failed to convert XML to HTML: {str(e)}")
    
    def flatten_xml(
        self,
        xml_content: str,
        separator: str = "."
    ) -> Dict[str, Any]:
        """
        Flatten nested XML structure into flat dictionary with dot notation
        
        Args:
            xml_content: XML string to flatten
            separator: Separator for nested keys
            
        Returns:
            Flattened dictionary
        """
        try:
            data = xmltodict.parse(xml_content)
            flattened = self._flatten_dict(data, separator=separator)
            
            self.logger.info("Successfully flattened XML")
            return flattened
            
        except Exception as e:
            self.logger.error(f"XML flattening failed: {str(e)}")
            raise ProcessingError(f"Failed to flatten XML: {str(e)}")
    
    def _flatten_dict(
        self,
        d: Dict[str, Any],
        parent_key: str = "",
        separator: str = "."
    ) -> Dict[str, Any]:
        """Recursively flatten nested dictionary"""
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}{separator}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(self._flatten_dict(v, new_key, separator).items())
            elif isinstance(v, list):
                for i, item in enumerate(v):
                    if isinstance(item, dict):
                        items.extend(
                            self._flatten_dict(item, f"{new_key}[{i}]", separator).items()
                        )
                    else:
                        items.append((f"{new_key}[{i}]", item))
            else:
                items.append((new_key, v))
        return dict(items)


# Made with Bob
    def get_sample_xml(self) -> str:
        """Get sample XML data for testing"""
        return """<?xml version="1.0" encoding="UTF-8"?>
<employees>
    <employee>
        <id>1</id>
        <name>John Doe</name>
        <email>john@example.com</email>
        <age>30</age>
        <city>New York</city>
    </employee>
    <employee>
        <id>2</id>
        <name>Jane Smith</name>
        <email>jane@example.com</email>
        <age>25</age>
        <city>Los Angeles</city>
    </employee>
    <employee>
        <id>3</id>
        <name>Bob Johnson</name>
        <email>bob@example.com</email>
        <age>35</age>
        <city>Chicago</city>
    </employee>
</employees>"""
