# JSON Toolkit API Documentation

Complete API reference for the JSON Toolkit module of the Enterprise Payload Utility Toolkit.

## Table of Contents

1. [Overview](#overview)
2. [Format & Validate](#format--validate)
3. [JSONPath Operations](#jsonpath-operations)
4. [Schema Operations](#schema-operations)
5. [Comparison Operations](#comparison-operations)
6. [Explorer Operations](#explorer-operations)
7. [Error Handling](#error-handling)
8. [Examples](#examples)

---

## Overview

The JSON Toolkit provides comprehensive JSON processing capabilities including formatting, validation, JSONPath queries, schema generation/validation, comparison, and structure exploration.

**Base URL**: `http://localhost:8000/api/v1/json`

**All endpoints accept**: `application/json`

**All endpoints return**: `application/json`

---

## Format & Validate

### 1. Format JSON

**Endpoint**: `POST /json/format`

Format and beautify JSON content with customizable indentation and options.

**Request Body**:
```json
{
  "json_content": "string (required)",
  "indent": 2,
  "sort_keys": false,
  "ensure_ascii": false
}
```

**Parameters**:
- `json_content` (string, required): JSON string to format
- `indent` (integer, optional): Number of spaces for indentation (0-8), default: 2
- `sort_keys` (boolean, optional): Sort object keys alphabetically, default: false
- `ensure_ascii` (boolean, optional): Escape non-ASCII characters, default: false

**Response**:
```json
{
  "formatted_json": "string",
  "status": "success"
}
```

**Example**:
```bash
curl -X POST "http://localhost:8000/api/v1/json/format" \
  -H "Content-Type: application/json" \
  -d '{
    "json_content": "{\"name\":\"John\",\"age\":30}",
    "indent": 4,
    "sort_keys": true
  }'
```

---

### 2. Validate JSON

**Endpoint**: `POST /json/validate`

Validate JSON syntax and structure.

**Request Body**:
```json
{
  "json_content": "string (required)"
}
```

**Response**:
```json
{
  "is_valid": true,
  "status": "success",
  "error": "string (optional)"
}
```

**Example**:
```bash
curl -X POST "http://localhost:8000/api/v1/json/validate" \
  -H "Content-Type: application/json" \
  -d '{
    "json_content": "{\"name\": \"John\", \"age\": 30}"
  }'
```

---

### 3. Minify JSON

**Endpoint**: `POST /json/minify`

Remove all unnecessary whitespace from JSON.

**Request Body**:
```json
{
  "json_content": "string (required)"
}
```

**Response**:
```json
{
  "minified_json": "string",
  "status": "success"
}
```

**Example**:
```bash
curl -X POST "http://localhost:8000/api/v1/json/minify" \
  -H "Content-Type: application/json" \
  -d '{
    "json_content": "{\n  \"name\": \"John\",\n  \"age\": 30\n}"
  }'
```

---

## JSONPath Operations

### 4. Execute JSONPath Query

**Endpoint**: `POST /json/jsonpath/execute`

Execute JSONPath expressions to query JSON data.

**Request Body**:
```json
{
  "json_content": "string (required)",
  "jsonpath_query": "string (required)",
  "use_extended": false
}
```

**Parameters**:
- `json_content` (string, required): JSON string to query
- `jsonpath_query` (string, required): JSONPath expression (e.g., "$.users[*].name")
- `use_extended` (boolean, optional): Use extended JSONPath syntax, default: false

**Response**:
```json
{
  "matches": ["array of matched values"],
  "match_count": 0,
  "status": "success"
}
```

**JSONPath Syntax Examples**:
- `$` - Root object
- `$.store.book[*]` - All books in store
- `$..author` - All authors (recursive descent)
- `$.store.book[0]` - First book
- `$.store.book[-1]` - Last book
- `$.store.book[0:2]` - First two books
- `$.store.book[?(@.price < 10)]` - Books with price < 10

**Example**:
```bash
curl -X POST "http://localhost:8000/api/v1/json/jsonpath/execute" \
  -H "Content-Type: application/json" \
  -d '{
    "json_content": "{\"users\": [{\"name\": \"John\", \"age\": 30}, {\"name\": \"Jane\", \"age\": 25}]}",
    "jsonpath_query": "$.users[*].name"
  }'
```

---

### 5. Find by Key

**Endpoint**: `POST /json/jsonpath/find-key`

Find all occurrences of a specific key in JSON structure.

**Query Parameters**:
- `json_content` (string, required): JSON string to search
- `key_name` (string, required): Key name to find
- `case_sensitive` (boolean, optional): Case-sensitive search, default: true

**Response**:
```json
{
  "results": [
    {
      "path": "$.users[0].name",
      "value": "John"
    }
  ],
  "count": 1,
  "status": "success"
}
```

**Example**:
```bash
curl -X POST "http://localhost:8000/api/v1/json/jsonpath/find-key?key_name=email&case_sensitive=false" \
  -H "Content-Type: application/json" \
  -d '{"json_content": "{\"user\": {\"Email\": \"test@example.com\"}}"}'
```

---

## Schema Operations

### 6. Generate JSON Schema

**Endpoint**: `POST /json/schema/generate`

Generate JSON Schema from sample JSON data.

**Request Body**:
```json
{
  "json_content": "string (required)",
  "title": "string (optional)",
  "description": "string (optional)"
}
```

**Response**:
```json
{
  "schema": {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {},
    "required": []
  },
  "status": "success"
}
```

**Example**:
```bash
curl -X POST "http://localhost:8000/api/v1/json/schema/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "json_content": "{\"name\": \"John\", \"age\": 30, \"email\": \"john@example.com\"}",
    "title": "User Schema",
    "description": "Schema for user objects"
  }'
```

---

### 7. Validate Against Schema

**Endpoint**: `POST /json/schema/validate`

Validate JSON data against a JSON Schema.

**Request Body**:
```json
{
  "json_content": "string (required)",
  "schema": {
    "type": "object",
    "properties": {},
    "required": []
  }
}
```

**Response**:
```json
{
  "valid": true,
  "error_count": 0,
  "errors": [],
  "status": "success"
}
```

**Example**:
```bash
curl -X POST "http://localhost:8000/api/v1/json/schema/validate" \
  -H "Content-Type: application/json" \
  -d '{
    "json_content": "{\"name\": \"John\", \"age\": 30}",
    "schema": {
      "type": "object",
      "properties": {
        "name": {"type": "string"},
        "age": {"type": "integer"}
      },
      "required": ["name", "age"]
    }
  }'
```

---

## Comparison Operations

### 8. Compare JSON Documents

**Endpoint**: `POST /json/diff/compare`

Compare two JSON documents and identify differences.

**Request Body**:
```json
{
  "json1": "string (required)",
  "json2": "string (required)",
  "ignore_order": false,
  "ignore_string_case": false
}
```

**Parameters**:
- `json1` (string, required): First JSON document
- `json2` (string, required): Second JSON document
- `ignore_order` (boolean, optional): Ignore array element order, default: false
- `ignore_string_case` (boolean, optional): Ignore string case differences, default: false

**Response**:
```json
{
  "identical": false,
  "differences": {
    "values_changed": {},
    "dictionary_item_added": [],
    "dictionary_item_removed": [],
    "type_changes": {},
    "iterable_item_added": {},
    "iterable_item_removed": {}
  },
  "summary": {
    "total_changes": 5,
    "values_changed": 2,
    "items_added": 1,
    "items_removed": 1,
    "type_changes": 1
  },
  "status": "success"
}
```

**Example**:
```bash
curl -X POST "http://localhost:8000/api/v1/json/diff/compare" \
  -H "Content-Type: application/json" \
  -d '{
    "json1": "{\"name\": \"John\", \"age\": 30}",
    "json2": "{\"name\": \"Jane\", \"age\": 25, \"city\": \"NYC\"}",
    "ignore_order": false
  }'
```

---

## Explorer Operations

### 9. Get Structure

**Endpoint**: `POST /json/explore/structure`

Get hierarchical structure of JSON document.

**Request Body**:
```json
{
  "json_content": "string (required)",
  "max_depth": 10
}
```

**Parameters**:
- `json_content` (string, required): JSON string to analyze
- `max_depth` (integer, optional): Maximum depth to traverse, default: 10

**Response**:
```json
{
  "structure": {
    "type": "object",
    "keys": ["name", "age", "address"],
    "children": {}
  },
  "status": "success"
}
```

**Example**:
```bash
curl -X POST "http://localhost:8000/api/v1/json/explore/structure" \
  -H "Content-Type: application/json" \
  -d '{
    "json_content": "{\"user\": {\"name\": \"John\", \"contacts\": {\"email\": \"john@example.com\"}}}",
    "max_depth": 5
  }'
```

---

### 10. Get Statistics

**Endpoint**: `POST /json/explore/statistics`

Get comprehensive statistics about JSON document.

**Request Body**:
```json
{
  "json_content": "string (required)"
}
```

**Response**:
```json
{
  "statistics": {
    "total_keys": 10,
    "total_values": 10,
    "max_depth": 3,
    "total_objects": 2,
    "total_arrays": 1,
    "total_strings": 5,
    "total_numbers": 2,
    "total_booleans": 1,
    "total_nulls": 0,
    "size_bytes": 256
  },
  "status": "success"
}
```

**Example**:
```bash
curl -X POST "http://localhost:8000/api/v1/json/explore/statistics" \
  -H "Content-Type: application/json" \
  -d '{
    "json_content": "{\"users\": [{\"name\": \"John\", \"age\": 30}, {\"name\": \"Jane\", \"age\": 25}]}"
  }'
```

---

### 11. Flatten JSON

**Endpoint**: `POST /json/flatten`

Flatten nested JSON structure into dot-notation keys.

**Request Body**:
```json
{
  "json_content": "string (required)",
  "separator": "."
}
```

**Parameters**:
- `json_content` (string, required): JSON string to flatten
- `separator` (string, optional): Key separator, default: "."

**Response**:
```json
{
  "flattened": {
    "user.name": "John",
    "user.age": 30,
    "user.address.city": "NYC"
  },
  "status": "success"
}
```

**Example**:
```bash
curl -X POST "http://localhost:8000/api/v1/json/flatten" \
  -H "Content-Type: application/json" \
  -d '{
    "json_content": "{\"user\": {\"name\": \"John\", \"address\": {\"city\": \"NYC\"}}}",
    "separator": "."
  }'
```

---

## Error Handling

All endpoints follow consistent error handling:

### Validation Errors (400)
```json
{
  "detail": "Invalid JSON syntax: Expecting property name enclosed in double quotes"
}
```

### Processing Errors (400)
```json
{
  "detail": "JSONPath query execution failed: Invalid expression"
}
```

### Server Errors (500)
```json
{
  "detail": "Internal server error: Unexpected error occurred"
}
```

---

## Examples

### Complete Workflow Example

```python
import requests
import json

BASE_URL = "http://localhost:8000/api/v1/json"

# 1. Format JSON
json_data = '{"name":"John","age":30,"address":{"city":"NYC","zip":"10001"}}'
response = requests.post(
    f"{BASE_URL}/format",
    json={
        "json_content": json_data,
        "indent": 2,
        "sort_keys": True
    }
)
formatted = response.json()["formatted_json"]
print("Formatted JSON:", formatted)

# 2. Execute JSONPath query
response = requests.post(
    f"{BASE_URL}/jsonpath/execute",
    json={
        "json_content": formatted,
        "jsonpath_query": "$.address.city"
    }
)
matches = response.json()["matches"]
print("City:", matches[0])

# 3. Generate schema
response = requests.post(
    f"{BASE_URL}/schema/generate",
    json={
        "json_content": formatted,
        "title": "User Schema"
    }
)
schema = response.json()["schema"]
print("Generated Schema:", json.dumps(schema, indent=2))

# 4. Get statistics
response = requests.post(
    f"{BASE_URL}/explore/statistics",
    json={"json_content": formatted}
)
stats = response.json()["statistics"]
print(f"Total keys: {stats['total_keys']}")
print(f"Max depth: {stats['max_depth']}")

# 5. Flatten structure
response = requests.post(
    f"{BASE_URL}/flatten",
    json={
        "json_content": formatted,
        "separator": "."
    }
)
flattened = response.json()["flattened"]
print("Flattened:", json.dumps(flattened, indent=2))
```

### JSONPath Query Examples

```python
# Find all user names
jsonpath_query = "$.users[*].name"

# Find users older than 25
jsonpath_query = "$.users[?(@.age > 25)]"

# Get all email addresses recursively
jsonpath_query = "$..email"

# Get first and last items
jsonpath_query = "$.items[0,-1]"

# Get items with specific property
jsonpath_query = "$.products[?(@.inStock == true)]"
```

### Schema Validation Example

```python
# Generate schema from sample
sample_data = {
    "name": "John Doe",
    "age": 30,
    "email": "john@example.com",
    "active": True
}

response = requests.post(
    f"{BASE_URL}/schema/generate",
    json={
        "json_content": json.dumps(sample_data),
        "title": "User Schema"
    }
)
schema = response.json()["schema"]

# Validate new data against schema
new_data = {
    "name": "Jane Doe",
    "age": "25",  # Wrong type - should be integer
    "email": "jane@example.com"
}

response = requests.post(
    f"{BASE_URL}/schema/validate",
    json={
        "json_content": json.dumps(new_data),
        "schema": schema
    }
)
validation = response.json()
print(f"Valid: {validation['valid']}")
print(f"Errors: {validation['errors']}")
```

### Comparison Example

```python
# Compare two configurations
config_v1 = {
    "database": {
        "host": "localhost",
        "port": 5432,
        "name": "mydb"
    },
    "cache": {
        "enabled": True
    }
}

config_v2 = {
    "database": {
        "host": "prod-server",
        "port": 5432,
        "name": "mydb"
    },
    "cache": {
        "enabled": True,
        "ttl": 3600
    }
}

response = requests.post(
    f"{BASE_URL}/diff/compare",
    json={
        "json1": json.dumps(config_v1),
        "json2": json.dumps(config_v2),
        "ignore_order": False
    }
)
diff = response.json()
print(f"Identical: {diff['identical']}")
print(f"Changes: {diff['summary']['total_changes']}")
print("Differences:", json.dumps(diff['differences'], indent=2))
```

---

## Best Practices

1. **Large Files**: For files > 10MB, consider streaming or chunking
2. **JSONPath**: Test queries with simple data first
3. **Schema Generation**: Use representative sample data
4. **Comparison**: Use `ignore_order` for unordered arrays
5. **Validation**: Always validate before processing
6. **Error Handling**: Check response status codes
7. **Performance**: Minify JSON for network transfer
8. **Security**: Validate input size limits

---

## Performance Considerations

- **Format**: O(n) where n is JSON size
- **JSONPath**: O(n) for simple paths, O(n²) for recursive descent
- **Schema Generation**: O(n) single pass
- **Comparison**: O(n) where n is larger document size
- **Flatten**: O(n × d) where d is depth

---

## Related Documentation

- [XML Toolkit API](./XML_TOOLKIT.md)
- [Implementation Roadmap](./IMPLEMENTATION_ROADMAP.md)
- [Architecture Overview](./ARCHITECTURE.md)

---

**Made with Bob** 🤖