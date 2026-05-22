# Installation Guide - Enterprise Payload Utility Toolkit

## ✅ Dependencies Successfully Installed

The following core packages have been installed:

### Web Framework & API
- ✅ FastAPI 0.136.1 - Modern web framework
- ✅ Uvicorn 0.46.0 - ASGI server
- ✅ Starlette 1.0.0 - Web framework foundation

### Data Validation & Processing
- ✅ Pydantic 2.13.4 - Data validation
- ✅ Pydantic Settings 2.0.3 - Settings management

### XML & JSON Processing
- ✅ lxml 6.1.0 - XML parsing (pre-installed)
- ✅ xmltodict 1.0.4 - XML to dict conversion
- ✅ jsonpath-ng 1.8.0 - JSONPath queries

### YAML Processing
- ✅ PyYAML 6.0.3 - YAML parsing (pre-installed)

### Utilities
- ✅ deepdiff 9.0.0 - Deep comparison
- ✅ httpx 0.28.1 - HTTP client
- ✅ aiofiles 23.2.1 - Async file I/O
- ✅ cachetools 7.1.1 - Caching
- ✅ python-json-logger 4.1.0 - JSON logging
- ✅ python-dotenv 1.2.2 - Environment variables
- ✅ pygments 2.20.0 - Syntax highlighting
- ✅ python-dateutil 2.9.0 - Date utilities

## ⚠️ Optional Dependencies (Require Visual Studio Build Tools)

The following packages require C/C++ compilation and were **not installed**:

- ❌ pandas - Data analysis (requires numpy)
- ❌ streamlit - Web UI framework (requires numpy)
- ❌ regex - Advanced regex (requires compilation)
- ❌ ujson - Fast JSON (requires compilation)

### Why These Failed

Your system is missing **Microsoft Visual C++ Build Tools**, which are required to compile these packages from source.

### Option 1: Install Visual Studio Build Tools (Recommended for Full Features)

1. Download **Build Tools for Visual Studio 2022**:
   https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2022

2. Run the installer and select:
   - ✅ Desktop development with C++
   - ✅ MSVC v143 - VS 2022 C++ x64/x86 build tools
   - ✅ Windows 10/11 SDK

3. After installation, restart your terminal and run:
   ```bash
   pip install pandas streamlit regex ujson
   ```

### Option 2: Use Pre-built Wheels (Quick Alternative)

Install from pre-built wheels (if available for Python 3.13):

```bash
# Try installing with --only-binary flag
pip install --only-binary :all: pandas streamlit

# Or use conda (if you have it)
conda install pandas streamlit
```

### Option 3: Continue Without These Packages (Current Setup)

The toolkit **will work** without these packages, but with limitations:

**What Works:**
- ✅ All core utilities (exceptions, logging, file handling)
- ✅ XML parsing and processing
- ✅ JSON parsing and processing
- ✅ FastAPI backend (when implemented)
- ✅ Basic caching and utilities

**What's Limited:**
- ❌ Streamlit frontend (need alternative UI)
- ❌ Pandas-based log analysis (can use basic Python)
- ❌ Advanced regex features (can use standard `re` module)

## 🚀 Verify Installation

Test that the core packages work:

```python
# test_installation.py
from app.core.file_handler import FileHandler
from app.core.logger import setup_logging, get_logger
from app.services.xml.parser import XMLParser

# Setup logging
setup_logging(log_level="INFO")
logger = get_logger(__name__)

# Test file handler
handler = FileHandler()
logger.info("✅ FileHandler initialized")

# Test XML parser
parser = XMLParser(disable_xxe=True)
xml_content = """<?xml version="1.0"?>
<root>
    <message>Hello World</message>
</root>"""

try:
    root = parser.parse(xml_content)
    logger.info(f"✅ XML parsed successfully. Root tag: {parser.get_root_tag(xml_content)}")
    
    formatted = parser.format(xml_content, indent=2)
    logger.info("✅ XML formatted successfully")
    print("\nFormatted XML:")
    print(formatted)
    
    print("\n✅ All core components working!")
except Exception as e:
    logger.error(f"❌ Error: {e}")
```

Run the test:
```bash
python test_installation.py
```

## 📦 What's Next

### Immediate Next Steps

1. **Complete XML Toolkit** - Implement remaining services
2. **Build JSON Toolkit** - Parser, JSONPath, differ
3. **Create FastAPI Backend** - API routes and endpoints
4. **Alternative Frontend** - Since Streamlit requires compilation:
   - Option A: Use Flask/FastAPI templates
   - Option B: Build React frontend
   - Option C: Install Build Tools and use Streamlit

### Development Without Streamlit

You can still build the backend and use:

1. **FastAPI Swagger UI** - Built-in API documentation at `/docs`
2. **Postman/Insomnia** - API testing tools
3. **cURL** - Command-line API testing
4. **Custom HTML/JS Frontend** - Simple web interface

Example FastAPI endpoint (when implemented):
```bash
# Format XML via API
curl -X POST http://localhost:8000/api/v1/xml/format \
  -H "Content-Type: application/json" \
  -d '{"xml_content": "<root><child>value</child></root>", "indent": 2}'
```

## 🔧 Troubleshooting

### Issue: Import errors

**Solution:**
```bash
# Ensure you're in the project root
cd e:/Git Repo/Bob-a-thon/Bob_Utility

# Verify Python version
python --version  # Should be 3.12+

# Reinstall if needed
pip install -r requirements-minimal.txt
```

### Issue: Module not found

**Solution:**
```bash
# Add project to Python path (temporary)
set PYTHONPATH=%PYTHONPATH%;e:/Git Repo/Bob-a-thon/Bob_Utility

# Or use relative imports in your code
```

### Issue: Want to use Streamlit

**Solution:**
Install Visual Studio Build Tools (see Option 1 above) or use Python 3.11 which has more pre-built wheels available.

## 📚 Documentation

- [`README.md`](README.md) - Project overview
- [`ARCHITECTURE.md`](ARCHITECTURE.md) - System design
- [`GETTING_STARTED.md`](GETTING_STARTED.md) - Development guide
- [`IMPLEMENTATION_GUIDE.md`](IMPLEMENTATION_GUIDE.md) - Implementation details

## ✅ Summary

**Status**: Core dependencies installed successfully! ✅

**Ready for**:
- Backend development (FastAPI)
- XML/JSON processing
- Core utility usage
- API endpoint creation

**Requires Build Tools for**:
- Streamlit frontend
- Pandas data analysis
- Advanced regex features

You can proceed with backend development and use alternative frontend solutions!