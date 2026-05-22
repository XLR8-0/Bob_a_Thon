# 🛠️ Enterprise Payload Utility Toolkit

A secure, local-first developer utility toolkit for handling enterprise payloads like XML, JSON, logs, YAML, configs, and API responses. Built for developers, integration engineers, DevOps teams, and support engineers who need powerful tools without relying on external online services.

## ✨ Features

### 🔧 XML Toolkit
- **Format & Beautify**: Clean up messy XML with configurable indentation
- **XPath Finder**: Execute XPath queries with result highlighting
- **Tree Explorer**: Interactive XML tree navigation
- **XML Diff**: Compare two XML documents side-by-side
- **XSD Validation**: Validate XML against schemas
- **XML ↔ JSON**: Bidirectional conversion
- **Click-to-XPath**: Generate XPath by clicking nodes

### 📊 JSON Toolkit
- **Format & Beautify**: Pretty-print JSON with syntax highlighting
- **JSONPath Finder**: Execute JSONPath queries
- **Key Explorer**: Navigate nested JSON structures
- **Schema Generator**: Auto-generate JSON schemas
- **JSON Diff**: Deep comparison with visual diff

### 📝 Log Analyzer
- **Large File Support**: Efficiently parse multi-GB log files
- **Exception Grouping**: Group repeated exceptions with counts
- **Pattern Detection**: Identify common error patterns
- **Smart Summarization**: Generate concise log summaries
- **Stack Trace Highlighting**: Visual stack trace analysis

### 🔍 Regex Assistant
- **Pattern Generator**: Generate regex from examples
- **Pattern Validator**: Test and validate regex patterns
- **Plain English Explanation**: Understand complex regex
- **Live Testing**: Test patterns against sample text
- **Pattern Library**: Common regex patterns

### ⚙️ Config Comparator
- **Multi-Format Support**: Compare YAML, JSON, XML, ENV files
- **Missing Key Detection**: Find configuration gaps
- **Type Mismatch Detection**: Identify datatype inconsistencies
- **Environment Drift**: Detect config drift across environments

## 🚀 Quick Start

### Prerequisites
- Python 3.12 or higher
- pip package manager

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourorg/enterprise-payload-toolkit.git
cd enterprise-payload-toolkit
```

2. **Create virtual environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your preferences
```

### Running the Application

#### Option 1: Run Both Services (Recommended)
```bash
# Terminal 1 - Backend
python -m uvicorn app.main:app --reload --port 8000

# Terminal 2 - Frontend
streamlit run frontend/app.py --server.port 8501
```

#### Option 2: Using Scripts
```bash
# Windows
scripts\run_backend.bat
scripts\run_frontend.bat

# Linux/Mac
./scripts/run_backend.sh
./scripts/run_frontend.sh
```

#### Option 3: Docker
```bash
docker-compose up
```

### Access the Application
- **Frontend UI**: http://localhost:8501
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## 📁 Project Structure

```
enterprise-payload-toolkit/
├── app/                    # Backend (FastAPI)
│   ├── api/               # API endpoints
│   ├── services/          # Business logic
│   ├── core/              # Core utilities
│   └── main.py            # Application entry
├── frontend/              # Frontend (Streamlit)
│   ├── pages/             # UI pages
│   ├── components/        # Reusable components
│   └── app.py             # Frontend entry
├── tests/                 # Test suite
├── docs/                  # Documentation
└── examples/              # Sample payloads
```

## 🔧 Configuration

Key configuration options in `.env`:

```env
# File Upload
MAX_UPLOAD_SIZE_MB=50
ALLOWED_EXTENSIONS=".xml,.json,.yaml,.log"

# Security
DISABLE_XXE=true
MAX_RECURSION_DEPTH=100

# Performance
WORKER_PROCESSES=4
ENABLE_CACHING=true
```

## 📖 Usage Examples

### XML Formatting
```python
# Via API
curl -X POST http://localhost:8000/api/v1/xml/format \
  -H "Content-Type: application/json" \
  -d '{"xml_content": "<root><child>value</child></root>", "indent": 2}'
```

### JSONPath Query
```python
# Via API
curl -X POST http://localhost:8000/api/v1/json/jsonpath \
  -H "Content-Type: application/json" \
  -d '{"json_content": {...}, "jsonpath": "$.users[*].name"}'
```

### Log Analysis
```python
# Via API
curl -X POST http://localhost:8000/api/v1/logs/analyze \
  -F "file=@application.log"
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov=frontend --cov-report=html

# Run specific test suite
pytest tests/unit/test_xml_services.py

# Run integration tests
pytest tests/integration/
```

## 🏗️ Development

### Setup Development Environment
```bash
pip install -r requirements-dev.txt
pre-commit install
```

### Code Quality
```bash
# Format code
black app/ frontend/

# Sort imports
isort app/ frontend/

# Lint
flake8 app/ frontend/
pylint app/ frontend/

# Type checking
mypy app/ frontend/
```

### Adding a New Feature
1. Create service in `app/services/`
2. Add API endpoint in `app/api/v1/endpoints/`
3. Create frontend page in `frontend/pages/`
4. Add tests in `tests/`
5. Update documentation

## 📚 Documentation

- [Architecture Guide](ARCHITECTURE.md)
- [Project Structure](PROJECT_STRUCTURE.md)
- [API Reference](docs/api_reference.md)
- [User Guide](docs/user_guide.md)
- [Developer Guide](docs/developer_guide.md)
- [Deployment Guide](docs/deployment.md)

## 🔒 Security

This toolkit is designed for **local, offline use** with enterprise security in mind:

- ✅ No external API calls
- ✅ No data transmission to external servers
- ✅ XXE attack prevention
- ✅ Input validation and sanitization
- ✅ Secure file handling
- ✅ No persistent storage of sensitive data

## 🎯 Roadmap

### Version 1.1
- [ ] SQL query formatter
- [ ] Base64 encoder/decoder
- [ ] JWT token decoder
- [ ] Hash generator

### Version 1.2
- [ ] Plugin system
- [ ] Batch processing
- [ ] API testing toolkit
- [ ] GraphQL formatter

### Version 2.0
- [ ] CLI interface
- [ ] History and favorites
- [ ] Custom templates
- [ ] Export capabilities

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- UI powered by [Streamlit](https://streamlit.io/)
- XML parsing by [lxml](https://lxml.de/)
- JSON processing by [jsonpath-ng](https://github.com/h2non/jsonpath-ng)

## 📧 Support

- 📖 [Documentation](https://enterprise-payload-toolkit.readthedocs.io)
- 🐛 [Issue Tracker](https://github.com/yourorg/enterprise-payload-toolkit/issues)
- 💬 [Discussions](https://github.com/yourorg/enterprise-payload-toolkit/discussions)

## ⭐ Star History

If you find this project useful, please consider giving it a star!

---

**Made with ❤️ for developers who value privacy and local-first tools**