# Regex Assistant Toolkit

## Overview

The Regex Assistant provides comprehensive tools for working with regular expressions, including pattern generation, validation, testing, and explanation.

## Features

### 1. Pattern Validation
- Syntax validation
- Pattern warnings and best practices
- Group detection (capturing and named groups)
- Flag analysis

### 2. Pattern Testing
- Multiple test operations (search, match, fullmatch, findall, finditer)
- Batch testing against multiple strings
- Performance testing with metrics
- Detailed match information with positions and groups

### 3. Pattern Explanation
- Human-readable pattern breakdown
- Component-by-component explanation
- Complexity assessment
- Pattern summary generation

### 4. Pattern Generation
- Generate from example strings
- 25+ common pattern templates
- Custom pattern generation from requirements
- Pattern type detection

### 5. Advanced Operations
- Find all matches with positions
- Replace matches with substitution
- Split text using patterns
- Performance benchmarking

## API Endpoints

### Validate Pattern
```http
POST /api/v1/regex/validate
Content-Type: application/json

{
  "pattern": "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"
}
```

**Response:**
```json
{
  "pattern": "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$",
  "is_valid": true,
  "error": null,
  "flags_used": [],
  "groups_count": 0,
  "named_groups": [],
  "warnings": []
}
```

### Test Pattern
```http
POST /api/v1/regex/test
Content-Type: application/json

{
  "pattern": "\\d{3}-\\d{2}-\\d{4}",
  "test_string": "123-45-6789",
  "flags": ["IGNORECASE"],
  "operation": "search"
}
```

**Response:**
```json
{
  "pattern": "\\d{3}-\\d{2}-\\d{4}",
  "is_valid": true,
  "test_string": "123-45-6789",
  "operation": "search",
  "flags": ["IGNORECASE"],
  "execution_time_ms": 0.123,
  "result": {
    "matched": true,
    "match": "123-45-6789",
    "start": 0,
    "end": 11,
    "groups": [],
    "named_groups": {}
  }
}
```

### Batch Test
```http
POST /api/v1/regex/test/batch
Content-Type: application/json

{
  "pattern": "^\\d{5}$",
  "test_strings": ["12345", "1234", "123456", "abcde"],
  "operation": "fullmatch"
}
```

**Response:**
```json
{
  "pattern": "^\\d{5}$",
  "operation": "fullmatch",
  "flags": [],
  "total_tests": 4,
  "matched_count": 1,
  "match_rate": 0.25,
  "total_execution_time_ms": 0.456,
  "average_execution_time_ms": 0.114,
  "results": [...]
}
```

### Explain Pattern
```http
POST /api/v1/regex/explain
Content-Type: application/json

{
  "pattern": "^[A-Z][a-z]+\\s[A-Z][a-z]+$"
}
```

**Response:**
```json
{
  "pattern": "^[A-Z][a-z]+\\s[A-Z][a-z]+$",
  "is_valid": true,
  "summary": "Match the entire string that contains: Start of string/line, Any character in: A through Z, ...",
  "breakdown": [
    {
      "token": "^",
      "type": "anchor",
      "explanation": "Start of string/line"
    },
    {
      "token": "[A-Z]",
      "type": "character_class",
      "explanation": "Any character in: A through Z"
    }
  ],
  "complexity": "medium"
}
```

### Generate from Examples
```http
POST /api/v1/regex/generate/from-examples
Content-Type: application/json

{
  "examples": ["john@example.com", "jane@test.org"],
  "pattern_type": "email"
}
```

**Response:**
```json
{
  "pattern": "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$",
  "pattern_type": "email",
  "confidence": "high",
  "matches_all_examples": true,
  "source": "common_pattern"
}
```

### Generate Custom Pattern
```http
POST /api/v1/regex/generate/custom
Content-Type: application/json

{
  "requirements": {
    "min_length": 8,
    "max_length": 20,
    "must_contain": ["digits", "lowercase", "uppercase"],
    "must_start_with": "A"
  }
}
```

**Response:**
```json
{
  "pattern": "^A[0-9a-zA-Z]{7,19}$",
  "requirements": {...},
  "confidence": "high",
  "source": "custom_requirements"
}
```

### Get Common Patterns
```http
GET /api/v1/regex/patterns/common
```

**Response:**
```json
{
  "patterns": {
    "email": "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$",
    "url": "^https?://...",
    "phone_us": "^(\\+1[-.\\s]?)?(\\(?\\d{3}\\)?[-.\\s]?)?\\d{3}[-.\\s]?\\d{4}$",
    ...
  },
  "count": 25
}
```

### Get Specific Common Pattern
```http
GET /api/v1/regex/patterns/common/email
```

**Response:**
```json
{
  "pattern_type": "email",
  "pattern": "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"
}
```

### Find All Matches
```http
POST /api/v1/regex/find-all
Content-Type: application/json

{
  "pattern": "\\d+",
  "text": "I have 3 apples and 5 oranges",
  "flags": []
}
```

**Response:**
```json
{
  "pattern": "\\d+",
  "is_valid": true,
  "text_length": 30,
  "matches_count": 2,
  "matches": [
    {
      "match": "3",
      "start": 7,
      "end": 8,
      "groups": [],
      "named_groups": {}
    },
    {
      "match": "5",
      "start": 20,
      "end": 21,
      "groups": [],
      "named_groups": {}
    }
  ]
}
```

### Replace Matches
```http
POST /api/v1/regex/replace
Content-Type: application/json

{
  "pattern": "\\d+",
  "text": "I have 3 apples and 5 oranges",
  "replacement": "X",
  "max_replacements": null
}
```

**Response:**
```json
{
  "pattern": "\\d+",
  "is_valid": true,
  "original_text": "I have 3 apples and 5 oranges",
  "result_text": "I have X apples and X oranges",
  "replacement": "X",
  "matches_before": 2,
  "replacements_made": 2,
  "matches_remaining": 0
}
```

### Split Text
```http
POST /api/v1/regex/split
Content-Type: application/json

{
  "pattern": "\\s+",
  "text": "Hello   world  from   regex",
  "maxsplit": 0
}
```

**Response:**
```json
{
  "pattern": "\\s+",
  "is_valid": true,
  "text": "Hello   world  from   regex",
  "maxsplit": 0,
  "flags": [],
  "execution_time_ms": 0.089,
  "parts_count": 4,
  "parts": ["Hello", "world", "from", "regex"]
}
```

### Performance Test
```http
POST /api/v1/regex/performance
Content-Type: application/json

{
  "pattern": "\\b\\w+@\\w+\\.\\w+\\b",
  "text": "Contact us at support@example.com or sales@test.org",
  "iterations": 1000
}
```

**Response:**
```json
{
  "pattern": "\\b\\w+@\\w+\\.\\w+\\b",
  "is_valid": true,
  "text_length": 52,
  "iterations": 1000,
  "flags": [],
  "average_time_ms": 0.045,
  "min_time_ms": 0.032,
  "max_time_ms": 0.156,
  "total_time_ms": 45.234,
  "performance_rating": "excellent"
}
```

## Common Pattern Types

The toolkit includes 25+ pre-built patterns:

### Communication
- `email` - Email addresses
- `url` - Web URLs
- `phone_us` - US phone numbers
- `phone_international` - International phone numbers

### Network
- `ipv4` - IPv4 addresses
- `ipv6` - IPv6 addresses
- `mac_address` - MAC addresses
- `domain` - Domain names

### Date/Time
- `date_iso` - ISO date format (YYYY-MM-DD)
- `date_us` - US date format (MM/DD/YYYY)
- `time_24h` - 24-hour time format
- `time_12h` - 12-hour time format with AM/PM

### Financial
- `credit_card` - Credit card numbers
- `ssn` - Social Security Numbers

### Location
- `zip_code` - US ZIP codes

### Web/Tech
- `hex_color` - Hexadecimal color codes
- `uuid` - UUID format
- `slug` - URL slugs
- `html_tag` - HTML tags

### Security
- `username` - Username format
- `password_strong` - Strong password requirements

### Numbers
- `number_integer` - Integer numbers
- `number_decimal` - Decimal numbers
- `number_positive` - Positive numbers

### Text
- `alphanumeric` - Alphanumeric characters only
- `letters_only` - Letters only
- `digits_only` - Digits only

## Regex Flags

Supported flags:
- `IGNORECASE` or `I` - Case-insensitive matching
- `MULTILINE` or `M` - ^ and $ match line boundaries
- `DOTALL` or `S` - . matches newlines
- `VERBOSE` or `X` - Ignore whitespace and comments
- `ASCII` or `A` - ASCII-only matching

## Performance Ratings

- `excellent` - < 0.1ms average
- `good` - 0.1-1ms average
- `acceptable` - 1-10ms average
- `slow` - 10-100ms average
- `very_slow` - > 100ms average

## Best Practices

### Pattern Writing
1. Use anchors (^ and $) when matching entire strings
2. Escape special characters with backslashes
3. Use non-capturing groups (?:) when you don't need the match
4. Be specific rather than overly broad
5. Test patterns with edge cases

### Performance
1. Avoid catastrophic backtracking patterns
2. Use atomic groups when appropriate
3. Place most specific alternatives first
4. Use word boundaries (\b) instead of \s when appropriate
5. Test performance with realistic data sizes

### Security
1. Validate input before applying regex
2. Set reasonable limits on input size
3. Use timeouts for complex patterns
4. Sanitize user-provided patterns
5. Be aware of ReDoS (Regular Expression Denial of Service) attacks

## Error Handling

All endpoints return structured error responses:

```json
{
  "status": "error",
  "error_code": "INVALID_PATTERN",
  "message": "Invalid regex pattern: unterminated character set at position 5",
  "details": {
    "pattern": "[abc",
    "position": 5
  }
}
```

Common error codes:
- `INVALID_PATTERN` - Syntax error in regex
- `VALIDATION_ERROR` - Request validation failed
- `TIMEOUT_ERROR` - Pattern execution timeout
- `INTERNAL_ERROR` - Server error

## Integration Examples

### Python
```python
import requests

# Validate a pattern
response = requests.post('http://localhost:8000/api/v1/regex/validate', 
    json={'pattern': r'\d{3}-\d{2}-\d{4}'})
result = response.json()
print(f"Valid: {result['is_valid']}")

# Test pattern
response = requests.post('http://localhost:8000/api/v1/regex/test',
    json={
        'pattern': r'\d{3}-\d{2}-\d{4}',
        'test_string': '123-45-6789',
        'operation': 'fullmatch'
    })
result = response.json()
print(f"Matched: {result['result']['matched']}")
```

### JavaScript
```javascript
// Explain a pattern
const response = await fetch('http://localhost:8000/api/v1/regex/explain', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
        pattern: '^[A-Z][a-z]+$'
    })
});
const result = await response.json();
console.log(result.summary);
```

### cURL
```bash
# Get common patterns
curl -X GET "http://localhost:8000/api/v1/regex/patterns/common"

# Generate pattern from examples
curl -X POST "http://localhost:8000/api/v1/regex/generate/from-examples" \
  -H "Content-Type: application/json" \
  -d '{"examples": ["test@example.com", "user@domain.org"], "pattern_type": "email"}'