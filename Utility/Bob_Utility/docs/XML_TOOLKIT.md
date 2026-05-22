# XML Toolkit - Complete Feature Documentation

**Enterprise Payload Utility Toolkit**  
**Version:** 1.0.0  
**Last Updated:** 2026-05-14

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [API Endpoints](#api-endpoints)
4. [Service Classes](#service-classes)
5. [Usage Examples](#usage-examples)
6. [Security Features](#security-features)

---

## 🎯 Overview

The XML Toolkit provides comprehensive XML processing capabilities for enterprise developers, including parsing, validation, transformation, comparison, and analysis. All operations run locally with no external dependencies.

### Key Benefits

- ✅ **Secure**: XXE attack prevention built-in
- ✅ **Local-First**: No external API calls
- ✅ **Fast**: Efficient lxml-based processing
- ✅ **Comprehensive**: 15+ XML operations
- ✅ **Enterprise-Ready**: Production-quality code

---

## 🚀 Features

### 1. XML Parser & Formatter
- Format and beautify XML with customizable indentation
- Validate XML syntax and well-formedness
- XXE (XML External Entity) attack prevention
- Custom encoding support

### 2. XPath Executor
- Execute XPath queries on XML documents
- Generate XPath expressions for elements
- Find elements by text content
- Find elements by attributes
- XPath syntax validation
- Namespace support

### 3. XML Tree Explorer
- Hierarchical tree structure visualization
- Document statistics (element count, depth, etc.)
- Navigate by path
- Find siblings and ancestors
- Configurable depth traversal

### 4. XML Differ
- Compare two XML documents
- Identify structural differences
- Value change detection
- Element addition/removal tracking
- Configurable comparison options
- Generate diff reports (text/HTML)

### 5. XSD Validator
- Validate XML against XSD schemas
- DTD validation support
- Generate XSD from XML structure
- Schema caching for performance
- Extract schema information

### 6. XML Converter
- XML ↔ JSON conversion
- XML ↔ YAML conversion
- XML → CSV conversion
- XML → HTML table conversion
- Flatten nested XML structures
- Bidirectional conversions

---

## 📡 API Endpoints

### Base URL
```
http://localhost:8000/api/v1/xml
```

### 1. Format & Validate

#### POST `/format`
Format and beautify XML content

**Request:**
```json
{
  "xml_content": "<root><item>value</item></root>",
  "indent": 2,
  "encoding": "utf-8",
  "xml_declaration": true
}
```

**Response:**
```json
{
  "formatted_xml": "<?xml version='1.0' encoding='utf-8'?>\n<root>\n  <item>value</item>\n</root>",
  "status": "success",
  "line_count": 3
}
```

#### POST `/validate`
Validate XML syntax

**Request:**
```json
{
  "xml_content": "<root><item>value</item></root>"
}
```

**Response:**
```json
{
  "is_valid": true,
  "status": "success",
  "error": null
}
```

### 2. XPath Operations

#### POST `/xpath/execute`
Execute XPath query

**Request:**
```json
{
  "xml_content": "<root><item id='1'>First</item><item id='2'>Second</item></root>",
  "xpath_query": "//item[@id='1']",
  "namespaces": null
}
```

**Response:**
```json
{
  "matches": [
    {
      "index": 0,
      "type": "element",
      "tag": "item",
      "text": "First",
      "attributes": {"id": "1"},
      "xpath": "/root/item[1]",
      "xml": "<item id=\"1\">First</item>"
    }
  ],
  "match_count": 1,
  "status": "success"
}
```

#### POST `/xpath/generate`
Generate XPath for element

**Request:**
```json
{
  "xml_content": "<root><child><grandchild>value</grandchild></child></root>",
  "element_path": "/root/child/grandchild",
  "use_position": true,
  "use_attributes": false
}
```

**Response:**
```json
{
  "xpath": "/root/child[1]/grandchild[1]",
  "status": "success"
}
```

### 3. Tree Explorer

#### POST `/tree/structure`
Get hierarchical tree structure

**Request:**
```json
{
  "xml_content": "<root><child attr='value'>text</child></root>",
  "max_depth": null,
  "include_attributes": true,
  "include_text": true
}
```

**Response:**
```json
{
  "tree": {
    "tag": "root",
    "path": "/root",
    "depth": 0,
    "has_children": true,
    "child_count": 1,
    "children": [
      {
        "tag": "child",
        "path": "/root/child",
        "depth": 1,
        "attributes": {"attr": "value"},
        "text": "text",
        "has_children": false
      }
    ]
  },
  "status": "success"
}
```

#### POST `/tree/statistics`
Get document statistics

**Request:**
```json
{
  "xml_content": "<root><child1/><child2/></root>"
}
```

**Response:**
```json
{
  "statistics": {
    "total_elements": 3,
    "max_depth": 1,
    "total_attributes": 0,
    "total_text_nodes": 0,
    "unique_tags": ["child1", "child2", "root"],
    "unique_tag_count": 3,
    "unique_attributes": [],
    "unique_attribute_count": 0,
    "namespaces": []
  },
  "status": "success"
}
```

### 4. XML Comparison

#### POST `/diff/compare`
Compare two XML documents

**Request:**
```json
{
  "xml1": "<root><item>value1</item></root>",
  "xml2": "<root><item>value2</item></root>",
  "ignore_order": false,
  "ignore_whitespace": true,
  "ignore_comments": true,
  "ignore_attributes": false
}
```

**Response:**
```json
{
  "identical": false,
  "differences": [
    {
      "type": "value_changed",
      "path": "root.item",
      "old_value": "value1",
      "new_value": "value2"
    }
  ],
  "summary": {
    "total_differences": 1,
    "values_changed": 1,
    "items_added": 0,
    "items_removed": 0,
    "type_changes": 0
  },
  "status": "success"
}
```

### 5. XSD Validation

#### POST `/xsd/validate`
Validate XML against XSD schema

**Request:**
```json
{
  "xml_content": "<root><item>value</item></root>",
  "xsd_content": "<?xml version='1.0'?><xs:schema xmlns:xs='http://www.w3.org/2001/XMLSchema'>...</xs:schema>",
  "cache_schema": true
}
```

**Response:**
```json
{
  "valid": true,
  "error_count": 0,
  "errors": [],
  "status": "success"
}
```

#### POST `/xsd/generate`
Generate XSD from XML

**Request:**
```json
{
  "xml_content": "<root><item>value</item></root>",
  "target_namespace": null
}
```

**Response:**
```json
{
  "xsd_content": "<?xml version='1.0' encoding='UTF-8'?>\n<xs:schema xmlns:xs='http://www.w3.org/2001/XMLSchema'>...</xs:schema>",
  "status": "success"
}
```

### 6. Format Conversion

#### POST `/convert/to-json`
Convert XML to JSON

**Request:**
```json
{
  "xml_content": "<root><item>value</item></root>",
  "pretty": true,
  "indent": 2
}
```

**Response:**
```json
{
  "json_content": "{\n  \"root\": {\n    \"item\": \"value\"\n  }\n}",
  "status": "success"
}
```

#### POST `/convert/to-yaml`
Convert XML to YAML

**Request:**
```json
{
  "xml_content": "<root><item>value</item></root>",
  "default_flow_style": false
}
```

**Response:**
```json
{
  "yaml_content": "root:\n  item: value\n",
  "status": "success"
}
```

#### POST `/convert/from-json`
Convert JSON to XML

**Request:**
```json
{
  "json_content": "{\"item\": \"value\"}",
  "root_tag": "root",
  "pretty": true,
  "indent": 2
}
```

**Response:**
```json
{
  "xml_content": "<?xml version='1.0' encoding='utf-8'?>\n<root>\n  <item>value</item>\n</root>",
  "status": "success"
}
```

#### POST `/convert/from-yaml`
Convert YAML to XML

**Request:**
```json
{
  "yaml_content": "item: value",
  "root_tag": "root",
  "pretty": true,
  "indent": 2
}
```

**Response:**
```json
{
  "xml_content": "<?xml version='1.0' encoding='utf-8'?>\n<root>\n  <item>value</item>\n</root>",
  "status": "success"
}
```

---

## 🔧 Service Classes

### XMLParser
**Location:** `app/services/xml/parser.py`

**Methods:**
- `format(xml_content, indent, encoding, xml_declaration)` - Format XML
- `validate(xml_content)` - Validate XML syntax
- `parse(xml_content)` - Parse XML to ElementTree

### XPathExecutor
**Location:** `app/services/xml/xpath_executor.py`

**Methods:**
- `execute_xpath(xml_content, xpath_query, namespaces)` - Execute XPath
- `generate_xpath(element, use_position, use_attributes)` - Generate XPath
- `find_elements_by_text(xml_content, search_text, case_sensitive)` - Text search
- `find_elements_by_attribute(xml_content, attr_name, attr_value)` - Attribute search
- `validate_xpath(xpath_query)` - Validate XPath syntax
- `get_xpath_suggestions(xml_content, partial_xpath)` - Get suggestions

### XMLTreeExplorer
**Location:** `app/services/xml/tree_explorer.py`

**Methods:**
- `get_tree_structure(xml_content, max_depth, include_attributes, include_text)` - Get tree
- `get_statistics(xml_content)` - Get statistics
- `find_node_by_path(xml_content, path)` - Find node
- `get_siblings(xml_content, element_path)` - Get siblings
- `get_ancestors(xml_content, element_path)` - Get ancestors

### XMLDiffer
**Location:** `app/services/xml/differ.py`

**Methods:**
- `compare_xml(xml1, xml2, ignore_order, ignore_whitespace, ignore_comments, ignore_attributes)` - Compare
- `compare_structure(xml1, xml2)` - Compare structure only
- `find_missing_elements(xml1, xml2)` - Find missing elements
- `generate_diff_report(xml1, xml2, format)` - Generate report

### XSDValidator
**Location:** `app/services/xml/validator.py`

**Methods:**
- `validate_against_xsd(xml_content, xsd_content, cache_schema)` - XSD validation
- `validate_well_formed(xml_content)` - Well-formed check
- `validate_against_dtd(xml_content, dtd_content)` - DTD validation
- `generate_xsd_from_xml(xml_content, target_namespace)` - Generate XSD
- `get_schema_info(xsd_content)` - Extract schema info
- `clear_cache()` - Clear schema cache

### XMLConverter
**Location:** `app/services/xml/converter.py`

**Methods:**
- `xml_to_json(xml_content, pretty, indent)` - XML to JSON
- `xml_to_dict(xml_content)` - XML to dict
- `xml_to_yaml(xml_content, default_flow_style)` - XML to YAML
- `json_to_xml(json_content, root_tag, pretty, indent)` - JSON to XML
- `dict_to_xml(data, root_tag, pretty, indent)` - Dict to XML
- `yaml_to_xml(yaml_content, root_tag, pretty, indent)` - YAML to XML
- `xml_to_csv(xml_content, delimiter, include_header)` - XML to CSV
- `xml_to_html_table(xml_content, table_class)` - XML to HTML
- `flatten_xml(xml_content, separator)` - Flatten XML

---

## 💡 Usage Examples

### Python Usage

```python
from app.services.xml import XMLParser, XPathExecutor, XMLConverter

# Format XML
parser = XMLParser(disable_xxe=True)
formatted = parser.format("<root><item>value</item></root>", indent=2)

# Execute XPath
executor = XPathExecutor()
matches = executor.execute_xpath(
    "<root><item id='1'>First</item></root>",
    "//item[@id='1']"
)

# Convert XML to JSON
converter = XMLConverter()
json_str = converter.xml_to_json("<root><item>value</item></root>")
```

### cURL Examples

```bash
# Format XML
curl -X POST http://localhost:8000/api/v1/xml/format \
  -H "Content-Type: application/json" \
  -d '{"xml_content":"<root><item>value</item></root>","indent":2}'

# Execute XPath
curl -X POST http://localhost:8000/api/v1/xml/xpath/execute \
  -H "Content-Type: application/json" \
  -d '{"xml_content":"<root><item>value</item></root>","xpath_query":"//item"}'

# Convert to JSON
curl -X POST http://localhost:8000/api/v1/xml/convert/to-json \
  -H "Content-Type: application/json" \
  -d '{"xml_content":"<root><item>value</item></root>","pretty":true}'
```

---

## 🔒 Security Features

### XXE Prevention
All XML parsing operations have XXE (XML External Entity) attack prevention enabled by default:

```python
parser = XMLParser(disable_xxe=True)  # Default
```

This prevents:
- External entity expansion
- DTD processing
- Network access during parsing
- Billion laughs attacks

### Input Validation
- All inputs are validated using Pydantic models
- Size limits enforced
- Encoding validation
- Syntax checking before processing

### Error Handling
- Comprehensive exception handling
- Detailed error messages
- No sensitive information in errors
- Proper HTTP status codes

---

## 📊 Performance Considerations

### Caching
- XSD schemas are cached for repeated validations
- Use `cache_schema=true` for better performance
- Clear cache with `XSDValidator.clear_cache()`

### Large Files
- Stream processing for large XML files
- Configurable depth limits for tree traversal
- Efficient XPath execution
- Memory-conscious operations

### Best Practices
1. Use appropriate depth limits for tree exploration
2. Enable schema caching for repeated validations
3. Use specific XPath queries instead of broad searches
4. Consider file size when converting formats

---

## 🎓 Additional Resources

- **API Documentation:** http://localhost:8000/docs
- **Source Code:** `app/services/xml/`
- **Tests:** `tests/services/xml/`
- **Examples:** `examples/xml/`

---

**Made with Bob** 🤖