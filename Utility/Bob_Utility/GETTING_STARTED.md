# 🚀 Getting Started with Enterprise Payload Utility Toolkit

This guide will help you set up and start developing the Enterprise Payload Utility Toolkit.

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.12+** - [Download Python](https://www.python.org/downloads/)
- **pip** - Python package manager (comes with Python)
- **Git** - [Download Git](https://git-scm.com/downloads)
- **VS Code** (Recommended) - [Download VS Code](https://code.visualstudio.com/)

## 🔧 Initial Setup

### Step 1: Clone or Navigate to Project

```bash
# If cloning from repository
git clone <repository-url>
cd enterprise-payload-toolkit

# Or if already in project directory
cd e:/Git Repo/Bob-a-thon/Bob_Utility
```

### Step 2: Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

### Step 3: Install Dependencies

```bash
# Install production dependencies
pip install -r requirements.txt

# Install development dependencies (for testing, linting, etc.)
pip install -r requirements-dev.txt

# Verify installation
pip list
```

### Step 4: Configure Environment

```bash
# Copy environment template
copy .env.example .env  # Windows
# OR
cp .env.example .env    # Linux/Mac

# Edit .env file with your preferred settings
# You can use notepad, vim, or any text editor
notepad .env  # Windows
```

Key settings in `.env`:
```env
# Backend Configuration
BACKEND_PORT=8000
BACKEND_RELOAD=true

# Frontend Configuration
FRONTEND_PORT=8501

# File Upload Configuration
MAX_UPLOAD_SIZE_MB=50

# Logging Configuration
LOG_LEVEL="INFO"
```

## 📁 Project Structure Overview

```
enterprise-payload-toolkit/
├── app/                    # Backend (FastAPI)
│   ├── core/              # ✅ Core utilities (COMPLETED)
│   ├── services/          # 🚧 Business logic (IN PROGRESS)
│   ├── api/               # ⏳ API endpoints (PENDING)
│   └── main.py            # ⏳ App entry point (PENDING)
├── frontend/              # ⏳ Streamlit UI (PENDING)
├── tests/                 # ⏳ Test suite (PENDING)
├── docs/                  # 📚 Documentation
└── examples/              # ⏳ Sample files (PENDING)
```

## 🎯 Current Project Status

### ✅ Completed (Ready to Use)

1. **Core Utilities** (`app/core/`)
   - Exception handling system
   - Logging configuration
   - Secure file handler
   - Parser and validator base classes
   - Caching utilities
   - Common utility functions

2. **Documentation**
   - Architecture design
   - Project structure
   - Implementation guide
   - README with features

3. **Configuration**
   - Requirements files
   - Project configuration (pyproject.toml)
   - Environment template
   - Git ignore rules

### 🚧 In Progress

1. **XML Toolkit** (`app/services/xml/`)
   - ✅ XML Parser (with XXE protection)
   - ⏳ XML Formatter
   - ⏳ XPath Executor
   - ⏳ Tree Explorer
   - ⏳ XML Differ
   - ⏳ XSD Validator
   - ⏳ XML/JSON Converter

### ⏳ Pending

1. JSON Toolkit
2. Log Analyzer
3. Regex Assistant
4. Config Comparator
5. FastAPI Backend
6. Streamlit Frontend
7. Tests & Examples

## 🧪 Testing Current Implementation

### Test Core Utilities

Create a test file `test_core.py`:

```python
from app.core.file_handler import FileHandler
from app.core.logger import setup_logging, get_logger
from app.services.xml.parser import XMLParser

# Setup logging
setup_logging(log_level="INFO")
logger = get_logger(__name__)

# Test file handler
handler = FileHandler()
logger.info("FileHandler initialized successfully")

# Test XML parser
parser = XMLParser(disable_xxe=True)
xml_content = """<?xml version="1.0"?>
<root>
    <child>Hello World</child>
</root>"""

try:
    root = parser.parse(xml_content)
    logger.info(f"XML parsed successfully. Root tag: {parser.get_root_tag(xml_content)}")
    
    formatted = parser.format(xml_content, indent=2)
    logger.info("XML formatted successfully")
    print(formatted)
except Exception as e:
    logger.error(f"Error: {e}")
```

Run the test:
```bash
python test_core.py
```

## 🔨 Development Workflow

### 1. Create a Feature Branch

```bash
git checkout -b feature/xml-formatter
```

### 2. Implement Your Feature

Follow the existing patterns in `app/core/` and `app/services/xml/parser.py`.

Example structure for a new service:

```python
"""
Your Service Description
"""

from app.core.exceptions import ProcessingError
from app.services.base import BaseService

class YourService(BaseService):
    """Your service class"""
    
    def __init__(self) -> None:
        super().__init__()
        # Your initialization
    
    def your_method(self, input_data: str) -> str:
        """
        Your method description
        
        Args:
            input_data: Description
            
        Returns:
            Description
            
        Raises:
            ProcessingError: When something fails
        """
        try:
            # Your implementation
            result = input_data.upper()
            self.logger.info("Operation successful")
            return result
        except Exception as e:
            self.logger.error(f"Operation failed: {e}")
            raise ProcessingError(f"Failed: {e}")
```

### 3. Write Tests

Create test file in `tests/unit/`:

```python
import pytest
from app.services.your_module import YourService

def test_your_service():
    service = YourService()
    result = service.your_method("test")
    assert result == "TEST"
```

### 4. Run Code Quality Checks

```bash
# Format code
black app/ tests/

# Sort imports
isort app/ tests/

# Lint
flake8 app/ tests/

# Type check
mypy app/
```

### 5. Commit and Push

```bash
git add .
git commit -m "feat: implement XML formatter service"
git push origin feature/xml-formatter
```

## 📚 Key Concepts

### 1. Exception Handling

All custom exceptions inherit from `BaseToolkitException`:

```python
from app.core.exceptions import XMLParsingError

try:
    # Your code
    pass
except XMLParsingError as e:
    # e.to_dict() returns API-ready error response
    error_response = e.to_dict()
```

### 2. Logging

Use the logger mixin or get_logger:

```python
from app.core.logger import LoggerMixin

class MyClass(LoggerMixin):
    def my_method(self):
        self.logger.info("Processing started")
        self.logger.error("Something went wrong")
```

### 3. File Handling

Always use FileHandler for secure file operations:

```python
from app.core.file_handler import FileHandler

handler = FileHandler(max_size_bytes=50*1024*1024)
content = handler.read_file("path/to/file.xml")
# Automatically validates size and extension
```

### 4. Caching

Use the cache decorator for expensive operations:

```python
from app.core.cache import cache_result

@cache_result(ttl=3600, maxsize=100)
def expensive_operation(data):
    # This result will be cached
    return processed_data
```

## 🎓 Learning Resources

### Internal Documentation
- [`ARCHITECTURE.md`](ARCHITECTURE.md) - System design and patterns
- [`PROJECT_STRUCTURE.md`](PROJECT_STRUCTURE.md) - Folder organization
- [`IMPLEMENTATION_GUIDE.md`](IMPLEMENTATION_GUIDE.md) - Development guide

### External Resources
- [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [lxml Tutorial](https://lxml.de/tutorial.html)
- [Pydantic Documentation](https://docs.pydantic.dev/)

## 🐛 Troubleshooting

### Issue: Import errors for lxml

**Solution:**
```bash
pip install lxml
# On Windows, you might need Visual C++ Build Tools
```

### Issue: Module not found errors

**Solution:**
```bash
# Ensure you're in the project root
cd e:/Git Repo/Bob-a-thon/Bob_Utility

# Ensure virtual environment is activated
# You should see (venv) in your prompt

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue: Type checking warnings

**Solution:**
These are expected for some libraries (lxml, streamlit) that have limited type stubs. You can ignore them or add type: ignore comments.

## 🎯 Next Steps

### For New Contributors

1. **Read the documentation**
   - Start with [`README.md`](README.md)
   - Review [`ARCHITECTURE.md`](ARCHITECTURE.md)
   - Check [`IMPLEMENTATION_GUIDE.md`](IMPLEMENTATION_GUIDE.md)

2. **Set up your environment**
   - Follow this guide
   - Test the existing code
   - Run the test script above

3. **Pick a task**
   - Check the TODO list in [`IMPLEMENTATION_GUIDE.md`](IMPLEMENTATION_GUIDE.md)
   - Start with completing XML Toolkit
   - Or implement JSON Toolkit

4. **Start coding**
   - Follow existing patterns
   - Write tests
   - Document your code

### For Project Leads

1. **Complete XML Toolkit**
   - Implement remaining services
   - Add comprehensive tests
   - Create examples

2. **Build FastAPI Backend**
   - Create main.py
   - Define API routes
   - Add middleware

3. **Develop Streamlit Frontend**
   - Create main app
   - Build toolkit pages
   - Add UI components

## 💬 Getting Help

- **Documentation**: Check the `docs/` folder
- **Code Examples**: Review existing implementations in `app/core/` and `app/services/`
- **Issues**: Create GitHub issues for bugs or questions
- **Discussions**: Use GitHub discussions for general questions

## ✅ Checklist

Before you start developing:

- [ ] Python 3.12+ installed
- [ ] Virtual environment created and activated
- [ ] Dependencies installed (requirements.txt)
- [ ] Environment configured (.env file)
- [ ] Documentation reviewed
- [ ] Test script runs successfully
- [ ] Code editor configured (VS Code recommended)

You're now ready to start developing! 🎉

---

**Happy Coding!** 🚀

For questions or issues, refer to [`IMPLEMENTATION_GUIDE.md`](IMPLEMENTATION_GUIDE.md) or create an issue.