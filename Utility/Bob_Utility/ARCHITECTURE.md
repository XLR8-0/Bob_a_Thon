# Enterprise Payload Utility Toolkit - Architecture Document

## 1. High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend Layer                           │
│              (Streamlit Web Interface)                       │
│  ┌──────────┬──────────┬──────────┬──────────┬──────────┐  │
│  │   XML    │   JSON   │   Log    │  Regex   │  Config  │  │
│  │ Toolkit  │ Toolkit  │ Analyzer │ Assistant│Comparator│  │
│  └──────────┴──────────┴──────────┴──────────┴──────────┘  │
└─────────────────────────────────────────────────────────────┘
                            ↕ HTTP/REST
┌─────────────────────────────────────────────────────────────┐
│                    API Gateway Layer                         │
│                    (FastAPI Backend)                         │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Route Controllers                        │  │
│  │  /xml  /json  /logs  /regex  /config                │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            ↕
┌─────────────────────────────────────────────────────────────┐
│                   Service Layer                              │
│  ┌──────────┬──────────┬──────────┬──────────┬──────────┐  │
│  │   XML    │   JSON   │   Log    │  Regex   │  Config  │  │
│  │ Service  │ Service  │ Service  │ Service  │ Service  │  │
│  └──────────┴──────────┴──────────┴──────────┴──────────┘  │
└─────────────────────────────────────────────────────────────┘
                            ↕
┌─────────────────────────────────────────────────────────────┐
│                   Core Utilities Layer                       │
│  ┌──────────┬──────────┬──────────┬──────────┬──────────┐  │
│  │  Parser  │  File    │ Validator│  Differ  │  Logger  │  │
│  │  Base    │ Handler  │          │          │          │  │
│  └──────────┴──────────┴──────────┴──────────┴──────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## 2. Design Patterns

### 2.1 Strategy Pattern
- Used for different parsing strategies (XML, JSON, YAML)
- Allows runtime selection of parsing algorithm

### 2.2 Factory Pattern
- Service factory for creating appropriate service instances
- Parser factory for instantiating correct parser

### 2.3 Singleton Pattern
- Configuration manager
- Logger instance

### 2.4 Facade Pattern
- Service layer acts as facade to complex parsing operations
- Simplifies API for frontend consumption

### 2.5 Repository Pattern
- File operations abstracted through FileHandler
- Consistent interface for file I/O

## 3. Technology Stack

### Backend
- **Framework**: FastAPI 0.109+
- **Python**: 3.12+
- **Validation**: Pydantic v2
- **Async**: asyncio, aiofiles

### Frontend
- **Framework**: Streamlit 1.30+
- **Styling**: Custom CSS for enterprise look
- **Components**: Native Streamlit + custom components

### Core Libraries
```python
lxml==5.1.0              # XML parsing
jsonpath-ng==1.6.1       # JSONPath queries
deepdiff==6.7.1          # Deep comparison
pandas==2.2.0            # Data manipulation
pydantic==2.5.3          # Data validation
PyYAML==6.0.1            # YAML parsing
xmltodict==0.13.0        # XML to dict conversion
regex==2023.12.25        # Advanced regex
```

## 4. Module Breakdown

### 4.1 XML Toolkit
**Features:**
- Format/beautify XML with configurable indentation
- XPath query execution with result highlighting
- Interactive tree explorer with node selection
- XML diff with visual comparison
- XSD schema validation
- XML ↔ JSON bidirectional conversion
- Click-to-generate XPath from tree view

**Core Classes:**
- `XMLParser`: Parse and validate XML
- `XPathExecutor`: Execute XPath queries
- `XMLFormatter`: Format and beautify
- `XMLDiffer`: Compare XML documents
- `XSDValidator`: Validate against schema
- `XMLConverter`: Convert to/from JSON

### 4.2 JSON Toolkit
**Features:**
- Format/beautify JSON with syntax highlighting
- JSONPath query execution
- Nested key explorer with path display
- JSON schema generation from sample
- JSON diff with structural comparison

**Core Classes:**
- `JSONParser`: Parse and validate JSON
- `JSONPathExecutor`: Execute JSONPath queries
- `JSONFormatter`: Format and beautify
- `JSONSchemaGenerator`: Generate schema
- `JSONDiffer`: Compare JSON documents

### 4.3 Log Analyzer
**Features:**
- Stream large log files efficiently
- Group repeated exceptions with count
- Pattern detection (errors, warnings, stack traces)
- Generate executive summary
- Timestamp extraction and sorting
- Stack trace highlighting

**Core Classes:**
- `LogParser`: Parse log entries
- `ExceptionGrouper`: Group similar exceptions
- `PatternDetector`: Detect common patterns
- `LogSummarizer`: Generate summaries
- `StackTraceAnalyzer`: Analyze stack traces

### 4.4 Regex Assistant
**Features:**
- Generate regex from examples
- Validate regex patterns
- Explain regex in plain English
- Test regex against sample text
- Common pattern library

**Core Classes:**
- `RegexGenerator`: Generate patterns
- `RegexValidator`: Validate patterns
- `RegexExplainer`: Explain patterns
- `RegexTester`: Test against samples

### 4.5 Config Comparator
**Features:**
- Compare configs across formats (YAML, JSON, XML, ENV)
- Detect missing keys
- Detect datatype mismatches
- Environment drift detection
- Generate diff reports

**Core Classes:**
- `ConfigParser`: Parse various formats
- `ConfigComparator`: Compare configs
- `DriftDetector`: Detect environment drift
- `ConfigNormalizer`: Normalize to common format

## 5. API Contract Examples

### 5.1 XML Endpoints

```python
POST /api/v1/xml/format
Request:
{
    "xml_content": "<root><child>value</child></root>",
    "indent": 2,
    "encoding": "utf-8"
}
Response:
{
    "formatted_xml": "...",
    "status": "success"
}

POST /api/v1/xml/xpath
Request:
{
    "xml_content": "...",
    "xpath_query": "//child[@id='1']"
}
Response:
{
    "results": [...],
    "count": 5,
    "matched_nodes": [...]
}

POST /api/v1/xml/diff
Request:
{
    "xml1": "...",
    "xml2": "..."
}
Response:
{
    "differences": [...],
    "summary": {...}
}
```

### 5.2 JSON Endpoints

```python
POST /api/v1/json/format
POST /api/v1/json/jsonpath
POST /api/v1/json/schema
POST /api/v1/json/diff
```

### 5.3 Log Endpoints

```python
POST /api/v1/logs/analyze
POST /api/v1/logs/group-exceptions
POST /api/v1/logs/summarize
```

## 6. Performance Optimization Strategies

### 6.1 Large File Handling
- Stream processing for files > 10MB
- Chunked reading with generators
- Memory-mapped files for very large logs
- Lazy evaluation of results

### 6.2 Caching
- LRU cache for repeated operations
- Result caching for expensive computations
- Session-based caching in frontend

### 6.3 Async Operations
- Async file I/O with aiofiles
- Concurrent processing with asyncio
- Background tasks for long operations

### 6.4 Optimization Techniques
- Use lxml (C-based) for XML parsing
- ujson for faster JSON operations
- Compiled regex patterns
- Efficient data structures (sets, dicts)

## 7. Security Considerations

### 7.1 Input Validation
- Pydantic models for all inputs
- File size limits (default: 50MB)
- Content type validation
- Sanitize user inputs

### 7.2 XML Security
- Disable external entity resolution (XXE prevention)
- Limit recursion depth
- Validate against DTD/XSD safely

### 7.3 File Handling
- Temporary file cleanup
- Secure file permissions
- No persistent storage of sensitive data
- Memory cleanup after processing

## 8. Error Handling Strategy

### 8.1 Error Categories
- `ValidationError`: Invalid input data
- `ParsingError`: Failed to parse content
- `ProcessingError`: Error during processing
- `ResourceError`: File/memory issues

### 8.2 Error Response Format
```python
{
    "status": "error",
    "error_code": "PARSE_001",
    "message": "Failed to parse XML",
    "details": {...},
    "timestamp": "2026-05-14T04:00:00Z"
}
```

## 9. Testing Strategy

### 9.1 Unit Tests
- Test each service independently
- Mock external dependencies
- Test edge cases and error conditions
- Aim for 80%+ coverage

### 9.2 Integration Tests
- Test API endpoints
- Test service interactions
- Test file handling

### 9.3 Performance Tests
- Benchmark large file processing
- Memory usage profiling
- Response time measurements

## 10. Deployment Architecture

### 10.1 Local Development
```bash
# Backend
uvicorn app.main:app --reload --port 8000

# Frontend
streamlit run frontend/app.py --server.port 8501
```

### 10.2 Production Deployment
- Docker containerization
- Docker Compose for multi-service
- Nginx reverse proxy (optional)
- Systemd service files

### 10.3 Packaging Options
- PyInstaller for standalone executable
- Docker image distribution
- Python package (pip installable)

## 11. Future Enhancement Roadmap

### Phase 2 Features
- SQL query formatter and validator
- Base64 encoder/decoder
- JWT token decoder
- Hash generator (MD5, SHA256, etc.)
- URL encoder/decoder
- Timestamp converter

### Phase 3 Features
- Plugin system for custom parsers
- Batch processing capabilities
- API testing toolkit
- GraphQL query formatter
- Protocol buffer viewer

### Phase 4 Features
- Collaborative features (share snippets)
- History and favorites
- Custom templates
- Export to various formats
- CLI interface

## 12. MVP Scope Definition

### Must Have (MVP)
1. XML Toolkit: Format, XPath, Tree Explorer
2. JSON Toolkit: Format, JSONPath, Diff
3. Log Analyzer: Basic parsing and grouping
4. Basic UI with file upload
5. Copy to clipboard functionality

### Should Have (Post-MVP)
1. XML: XSD validation, XML diff
2. JSON: Schema generation
3. Log: Advanced pattern detection
4. Regex Assistant (basic)
5. Dark/light mode

### Could Have (Future)
1. Config Comparator
2. Advanced regex features
3. Export capabilities
4. History tracking
5. Batch operations

## 13. Development Timeline

### Week 1: Foundation
- Project setup
- Core utilities
- Base classes

### Week 2: XML & JSON Toolkits
- XML service implementation
- JSON service implementation
- Basic API endpoints

### Week 3: Log Analyzer & UI
- Log analyzer service
- Streamlit UI foundation
- Integration

### Week 4: Polish & Testing
- Regex assistant
- Testing
- Documentation
- Deployment setup