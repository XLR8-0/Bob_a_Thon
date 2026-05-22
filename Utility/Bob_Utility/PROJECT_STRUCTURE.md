# Enterprise Payload Utility Toolkit - Project Structure

```
enterprise-payload-toolkit/
│
├── README.md                          # Project overview and quick start
├── ARCHITECTURE.md                    # Detailed architecture document
├── LICENSE                            # MIT License
├── .gitignore                         # Git ignore rules
├── .env.example                       # Environment variables template
├── requirements.txt                   # Python dependencies
├── requirements-dev.txt               # Development dependencies
├── setup.py                           # Package setup file
├── pyproject.toml                     # Modern Python project config
├── docker-compose.yml                 # Docker composition
├── Dockerfile                         # Docker image definition
│
├── app/                               # Backend application
│   ├── __init__.py
│   ├── main.py                        # FastAPI application entry point
│   ├── config.py                      # Configuration management
│   ├── dependencies.py                # Dependency injection
│   │
│   ├── api/                           # API layer
│   │   ├── __init__.py
│   │   ├── v1/                        # API version 1
│   │   │   ├── __init__.py
│   │   │   ├── router.py              # Main router
│   │   │   ├── endpoints/             # API endpoints
│   │   │   │   ├── __init__.py
│   │   │   │   ├── xml.py             # XML toolkit endpoints
│   │   │   │   ├── json.py            # JSON toolkit endpoints
│   │   │   │   ├── logs.py            # Log analyzer endpoints
│   │   │   │   ├── regex.py           # Regex assistant endpoints
│   │   │   │   └── config.py          # Config comparator endpoints
│   │   │   │
│   │   │   └── models/                # Pydantic models
│   │   │       ├── __init__.py
│   │   │       ├── requests.py        # Request models
│   │   │       ├── responses.py       # Response models
│   │   │       └── common.py          # Common models
│   │   │
│   │   └── middleware/                # Custom middleware
│   │       ├── __init__.py
│   │       ├── error_handler.py       # Global error handling
│   │       ├── logging.py             # Request logging
│   │       └── cors.py                # CORS configuration
│   │
│   ├── services/                      # Business logic layer
│   │   ├── __init__.py
│   │   ├── base.py                    # Base service class
│   │   │
│   │   ├── xml/                       # XML toolkit services
│   │   │   ├── __init__.py
│   │   │   ├── parser.py              # XML parsing
│   │   │   ├── formatter.py           # XML formatting
│   │   │   ├── xpath_executor.py      # XPath queries
│   │   │   ├── tree_explorer.py       # Tree navigation
│   │   │   ├── differ.py              # XML comparison
│   │   │   ├── validator.py           # XSD validation
│   │   │   └── converter.py           # XML/JSON conversion
│   │   │
│   │   ├── json/                      # JSON toolkit services
│   │   │   ├── __init__.py
│   │   │   ├── parser.py              # JSON parsing
│   │   │   ├── formatter.py           # JSON formatting
│   │   │   ├── jsonpath_executor.py   # JSONPath queries
│   │   │   ├── explorer.py            # Key explorer
│   │   │   ├── schema_generator.py    # Schema generation
│   │   │   └── differ.py              # JSON comparison
│   │   │
│   │   ├── logs/                      # Log analyzer services
│   │   │   ├── __init__.py
│   │   │   ├── parser.py              # Log parsing
│   │   │   ├── grouper.py             # Exception grouping
│   │   │   ├── pattern_detector.py    # Pattern detection
│   │   │   ├── summarizer.py          # Summary generation
│   │   │   └── stack_trace_analyzer.py # Stack trace analysis
│   │   │
│   │   ├── regex/                     # Regex assistant services
│   │   │   ├── __init__.py
│   │   │   ├── generator.py           # Pattern generation
│   │   │   ├── validator.py           # Pattern validation
│   │   │   ├── explainer.py           # Pattern explanation
│   │   │   └── tester.py              # Pattern testing
│   │   │
│   │   └── config/                    # Config comparator services
│   │       ├── __init__.py
│   │       ├── parser.py              # Multi-format parsing
│   │       ├── comparator.py          # Config comparison
│   │       ├── drift_detector.py      # Drift detection
│   │       └── normalizer.py          # Format normalization
│   │
│   ├── core/                          # Core utilities
│   │   ├── __init__.py
│   │   ├── exceptions.py              # Custom exceptions
│   │   ├── logger.py                  # Logging configuration
│   │   ├── file_handler.py            # File operations
│   │   ├── parser_base.py             # Base parser class
│   │   ├── validator_base.py          # Base validator class
│   │   ├── cache.py                   # Caching utilities
│   │   └── utils.py                   # Common utilities
│   │
│   └── schemas/                       # Data schemas
│       ├── __init__.py
│       ├── xml_schemas/               # XSD schemas
│       └── json_schemas/              # JSON schemas
│
├── frontend/                          # Streamlit frontend
│   ├── __init__.py
│   ├── app.py                         # Main Streamlit app
│   ├── config.py                      # Frontend configuration
│   │
│   ├── pages/                         # Streamlit pages
│   │   ├── 1_🔧_XML_Toolkit.py
│   │   ├── 2_📊_JSON_Toolkit.py
│   │   ├── 3_📝_Log_Analyzer.py
│   │   ├── 4_🔍_Regex_Assistant.py
│   │   └── 5_⚙️_Config_Comparator.py
│   │
│   ├── components/                    # Reusable UI components
│   │   ├── __init__.py
│   │   ├── file_uploader.py           # File upload component
│   │   ├── code_editor.py             # Code editor component
│   │   ├── diff_viewer.py             # Diff viewer component
│   │   ├── tree_viewer.py             # Tree viewer component
│   │   └── result_display.py          # Result display component
│   │
│   ├── utils/                         # Frontend utilities
│   │   ├── __init__.py
│   │   ├── api_client.py              # Backend API client
│   │   ├── session_state.py           # Session management
│   │   └── formatters.py              # Display formatters
│   │
│   └── static/                        # Static assets
│       ├── styles/
│       │   ├── main.css               # Main stylesheet
│       │   └── themes.css             # Theme definitions
│       └── images/
│           └── logo.png               # Application logo
│
├── tests/                             # Test suite
│   ├── __init__.py
│   ├── conftest.py                    # Pytest configuration
│   │
│   ├── unit/                          # Unit tests
│   │   ├── __init__.py
│   │   ├── test_xml_services.py
│   │   ├── test_json_services.py
│   │   ├── test_log_services.py
│   │   ├── test_regex_services.py
│   │   └── test_config_services.py
│   │
│   ├── integration/                   # Integration tests
│   │   ├── __init__.py
│   │   ├── test_api_endpoints.py
│   │   └── test_service_integration.py
│   │
│   └── fixtures/                      # Test fixtures
│       ├── sample_xml/
│       │   ├── valid.xml
│       │   ├── invalid.xml
│       │   └── schema.xsd
│       ├── sample_json/
│       │   ├── valid.json
│       │   └── invalid.json
│       ├── sample_logs/
│       │   ├── application.log
│       │   └── error.log
│       └── sample_configs/
│           ├── config.yaml
│           ├── config.json
│           └── config.xml
│
├── scripts/                           # Utility scripts
│   ├── setup.sh                       # Setup script
│   ├── run_backend.sh                 # Run backend server
│   ├── run_frontend.sh                # Run frontend server
│   ├── run_tests.sh                   # Run test suite
│   └── build_docker.sh                # Build Docker image
│
├── docs/                              # Documentation
│   ├── index.md                       # Documentation home
│   ├── getting_started.md             # Getting started guide
│   ├── api_reference.md               # API documentation
│   ├── user_guide.md                  # User guide
│   ├── developer_guide.md             # Developer guide
│   └── deployment.md                  # Deployment guide
│
└── examples/                          # Example payloads
    ├── xml_examples/
    │   ├── soap_request.xml
    │   ├── rest_response.xml
    │   └── config.xml
    ├── json_examples/
    │   ├── api_response.json
    │   ├── config.json
    │   └── nested_data.json
    ├── log_examples/
    │   ├── application.log
    │   ├── error_stack.log
    │   └── access.log
    └── config_examples/
        ├── dev.yaml
        ├── staging.yaml
        └── prod.yaml
```

## Key Design Decisions

### 1. Separation of Concerns
- **app/**: Backend logic completely separated
- **frontend/**: UI layer independent
- **tests/**: Comprehensive test coverage
- **docs/**: Documentation separate from code

### 2. Modular Service Architecture
- Each toolkit has its own service module
- Services are independent and reusable
- Easy to add new toolkits

### 3. API Versioning
- `/api/v1/` structure allows future versions
- Backward compatibility maintained

### 4. Configuration Management
- Environment-based configuration
- Separate dev/prod settings
- Secure credential handling

### 5. Testing Strategy
- Unit tests for individual services
- Integration tests for API endpoints
- Fixtures for consistent test data

### 6. Documentation
- Architecture documentation
- API reference
- User and developer guides
- Deployment instructions

### 7. Deployment Options
- Docker support for containerization
- Scripts for easy local development
- Production-ready configuration

## File Naming Conventions

- **Python files**: `snake_case.py`
- **Classes**: `PascalCase`
- **Functions/methods**: `snake_case()`
- **Constants**: `UPPER_SNAKE_CASE`
- **Private methods**: `_leading_underscore()`

## Import Organization

```python
# Standard library imports
import os
import sys
from typing import List, Dict, Optional

# Third-party imports
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Local application imports
from app.core.exceptions import ValidationError
from app.services.xml.parser import XMLParser
```

## Module Responsibilities

### Core Layer
- **exceptions.py**: Custom exception hierarchy
- **logger.py**: Centralized logging
- **file_handler.py**: Secure file operations
- **parser_base.py**: Abstract base for parsers
- **cache.py**: Caching mechanisms

### Service Layer
- Business logic implementation
- Data transformation
- Validation and processing
- No direct HTTP handling

### API Layer
- HTTP request/response handling
- Input validation via Pydantic
- Error handling and formatting
- Route definitions

### Frontend Layer
- User interface components
- API client for backend communication
- Session state management
- Display formatting