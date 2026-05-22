"""
API v1 endpoints
"""

from app.api.v1.endpoints.xml import router as xml_router
from app.api.v1.endpoints.json import router as json_router
from app.api.v1.endpoints.regex import router as regex_router

__all__ = ["xml_router", "json_router", "regex_router"]

# Made with Bob
