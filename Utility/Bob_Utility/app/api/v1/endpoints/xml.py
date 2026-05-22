"""
XML Toolkit API endpoints
"""

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from app.api.v1.models import (
    XMLFormatRequest,
    XMLFormatResponse,
    XMLValidateRequest,
    XMLValidateResponse,
    XPathExecuteRequest,
    XPathExecuteResponse,
    XPathGenerateRequest,
    XPathGenerateResponse,
    XPathFindByValueRequest,
    XPathFindByValueResponse,
    TreeStructureRequest,
    TreeStructureResponse,
    TreeStatisticsRequest,
    TreeStatisticsResponse,
    XMLCompareRequest,
    XMLCompareResponse,
    XSDValidateRequest,
    XSDValidateResponse,
    XSDGenerateRequest,
    XSDGenerateResponse,
    XMLToJSONRequest,
    XMLToJSONResponse,
    XMLToYAMLRequest,
    XMLToYAMLResponse,
    JSONToXMLRequest,
    JSONToXMLResponse,
    YAMLToXMLRequest,
    YAMLToXMLResponse,
)
from app.core.exceptions import XMLParsingError, ValidationError, ProcessingError
from app.services.xml.parser import XMLParser
from app.services.xml.xpath_executor import XPathExecutor
from app.services.xml.tree_explorer import XMLTreeExplorer
from app.services.xml.differ import XMLDiffer
from app.services.xml.validator import XSDValidator
from app.services.xml.converter import XMLConverter

router = APIRouter(prefix="/xml", tags=["XML Toolkit"])


@router.post("/format", response_model=XMLFormatResponse)
async def format_xml(request: XMLFormatRequest) -> XMLFormatResponse:
    """
    Format and beautify XML content
    
    - **xml_content**: XML string to format
    - **indent**: Number of spaces for indentation (0-8)
    - **encoding**: Output encoding (default: utf-8)
    - **xml_declaration**: Include XML declaration (default: true)
    """
    try:
        parser = XMLParser(disable_xxe=True)
        formatted = parser.format(
            request.xml_content,
            indent=request.indent,
            encoding=request.encoding,
            xml_declaration=request.xml_declaration,
        )
        
        line_count = len(formatted.splitlines())
        
        return XMLFormatResponse(
            formatted_xml=formatted,
            status="success",
            line_count=line_count,
        )
    except XMLParsingError as e:
        raise HTTPException(status_code=400, detail=e.to_dict())
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "status": "error",
                "error_code": "INTERNAL_ERROR",
                "message": str(e),
            },
        )


@router.post("/validate", response_model=XMLValidateResponse)
async def validate_xml(request: XMLValidateRequest) -> XMLValidateResponse:
    """
    Validate XML content
    
    - **xml_content**: XML string to validate
    """
    try:
        parser = XMLParser(disable_xxe=True)
        is_valid = parser.validate(request.xml_content)
        
        if is_valid:
            return XMLValidateResponse(
                is_valid=True,
                status="success",
            )
        else:
            return XMLValidateResponse(
                is_valid=False,
                status="success",
                error="XML is not valid",
            )
    except XMLParsingError as e:
        return XMLValidateResponse(
            is_valid=False,
            status="success",
            error=e.message,
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "status": "error",
                "error_code": "INTERNAL_ERROR",
                "message": str(e),
            },
        )


# XPath Endpoints
@router.post("/xpath/execute", response_model=XPathExecuteResponse)
async def execute_xpath(request: XPathExecuteRequest) -> XPathExecuteResponse:
    """
    Execute XPath query on XML content
    
    - **xml_content**: XML string to query
    - **xpath_query**: XPath expression to execute
    - **namespaces**: Optional namespace mappings
    """
    try:
        executor = XPathExecutor()
        matches = executor.execute_xpath(
            request.xml_content,
            request.xpath_query,
            request.namespaces
        )
        
        return XPathExecuteResponse(
            matches=matches,
            match_count=len(matches),
            status="success"
        )
    except (ValidationError, ProcessingError) as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/xpath/generate", response_model=XPathGenerateResponse)
async def generate_xpath(request: XPathGenerateRequest) -> XPathGenerateResponse:
    """
    Generate XPath expression for an element
    
    - **xml_content**: XML content
    - **element_path**: Path to element
    - **use_position**: Include position predicates
    - **use_attributes**: Use attribute predicates
    """
    try:
        from lxml import etree
        executor = XPathExecutor()
        
        # Parse XML and find element
        root = etree.fromstring(request.xml_content.encode('utf-8'))
        # For now, generate XPath for root
        xpath = executor.generate_xpath(root, request.use_position, request.use_attributes)
        
        return XPathGenerateResponse(
            xpath=xpath,
            status="success"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/xpath/find-by-value", response_model=XPathFindByValueResponse)
async def find_xpath_by_value(request: XPathFindByValueRequest) -> XPathFindByValueResponse:
    """
    Find XPath expressions by searching for element values
    
    - **xml_content**: XML content to search
    - **search_value**: Value to search for in element text
    - **case_sensitive**: Whether search is case-sensitive (default: false)
    - **exact_match**: Whether to match exact value or use contains (default: false)
    """
    try:
        executor = XPathExecutor()
        matches = executor.find_by_value(
            request.xml_content,
            request.search_value,
            request.case_sensitive,
            request.exact_match
        )
        
        return XPathFindByValueResponse(
            matches=matches,
            match_count=len(matches),
            status="success"
        )
    except (ValidationError, ProcessingError) as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Tree Explorer Endpoints
@router.post("/tree/structure", response_model=TreeStructureResponse)
async def get_tree_structure(request: TreeStructureRequest) -> TreeStructureResponse:
    """
    Get hierarchical tree structure of XML document
    
    - **xml_content**: XML string to analyze
    - **max_depth**: Maximum depth to traverse
    - **include_attributes**: Include element attributes
    - **include_text**: Include element text content
    """
    try:
        explorer = XMLTreeExplorer()
        tree = explorer.get_tree_structure(
            request.xml_content,
            request.max_depth,
            request.include_attributes,
            request.include_text
        )
        
        return TreeStructureResponse(
            tree=tree,
            status="success"
        )
    except (ValidationError, ProcessingError) as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/tree/statistics", response_model=TreeStatisticsResponse)
async def get_tree_statistics(request: TreeStatisticsRequest) -> TreeStatisticsResponse:
    """
    Get statistics about XML document structure
    
    - **xml_content**: XML string to analyze
    """
    try:
        explorer = XMLTreeExplorer()
        statistics = explorer.get_statistics(request.xml_content)
        
        return TreeStatisticsResponse(
            statistics=statistics,
            status="success"
        )
    except (ValidationError, ProcessingError) as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# XML Differ Endpoints
@router.post("/diff/compare", response_model=XMLCompareResponse)
async def compare_xml(request: XMLCompareRequest) -> XMLCompareResponse:
    """
    Compare two XML documents
    
    - **xml1**: First XML content
    - **xml2**: Second XML content
    - **ignore_order**: Ignore element order
    - **ignore_whitespace**: Ignore whitespace differences
    - **ignore_comments**: Ignore XML comments
    - **ignore_attributes**: Ignore attribute differences
    """
    try:
        differ = XMLDiffer()
        result = differ.compare_xml(
            request.xml1,
            request.xml2,
            request.ignore_order,
            request.ignore_whitespace,
            request.ignore_comments,
            request.ignore_attributes
        )
        
        return XMLCompareResponse(
            identical=result["identical"],
            differences=result["differences"],
            summary=result["summary"],
            status="success"
        )
    except (ValidationError, ProcessingError) as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# XSD Validator Endpoints
@router.post("/xsd/validate", response_model=XSDValidateResponse)
async def validate_xsd(request: XSDValidateRequest) -> XSDValidateResponse:
    """
    Validate XML against XSD schema
    
    - **xml_content**: XML content to validate
    - **xsd_content**: XSD schema content
    - **cache_schema**: Cache compiled schema
    """
    try:
        validator = XSDValidator()
        result = validator.validate_against_xsd(
            request.xml_content,
            request.xsd_content,
            request.cache_schema
        )
        
        return XSDValidateResponse(
            valid=result["valid"],
            error_count=result["error_count"],
            errors=result["errors"],
            status="success"
        )
    except (ValidationError, ProcessingError) as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/xsd/generate", response_model=XSDGenerateResponse)
async def generate_xsd(request: XSDGenerateRequest) -> XSDGenerateResponse:
    """
    Generate XSD schema from XML structure
    
    - **xml_content**: XML content to analyze
    - **target_namespace**: Optional target namespace for schema
    """
    try:
        validator = XSDValidator()
        xsd_content = validator.generate_xsd_from_xml(
            request.xml_content,
            request.target_namespace
        )
        
        return XSDGenerateResponse(
            xsd_content=xsd_content,
            status="success"
        )
    except (ValidationError, ProcessingError) as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# XML Converter Endpoints
@router.post("/convert/to-json", response_model=XMLToJSONResponse)
async def xml_to_json(request: XMLToJSONRequest) -> XMLToJSONResponse:
    """
    Convert XML to JSON
    
    - **xml_content**: XML string to convert
    - **pretty**: Format JSON with indentation
    - **indent**: Number of spaces for indentation
    """
    try:
        converter = XMLConverter()
        json_content = converter.xml_to_json(
            request.xml_content,
            request.pretty,
            request.indent
        )
        
        return XMLToJSONResponse(
            json_content=json_content,
            status="success"
        )
    except (ValidationError, ProcessingError) as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/convert/to-yaml", response_model=XMLToYAMLResponse)
async def xml_to_yaml(request: XMLToYAMLRequest) -> XMLToYAMLResponse:
    """
    Convert XML to YAML
    
    - **xml_content**: XML string to convert
    - **default_flow_style**: YAML flow style setting
    """
    try:
        converter = XMLConverter()
        yaml_content = converter.xml_to_yaml(
            request.xml_content,
            request.default_flow_style
        )
        
        return XMLToYAMLResponse(
            yaml_content=yaml_content,
            status="success"
        )
    except (ValidationError, ProcessingError) as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/convert/from-json", response_model=JSONToXMLResponse)
async def json_to_xml(request: JSONToXMLRequest) -> JSONToXMLResponse:
    """
    Convert JSON to XML
    
    - **json_content**: JSON string to convert
    - **root_tag**: Root element tag name
    - **pretty**: Format XML with indentation
    - **indent**: Number of spaces for indentation
    """
    try:
        converter = XMLConverter()
        xml_content = converter.json_to_xml(
            request.json_content,
            request.root_tag,
            request.pretty,
            request.indent
        )
        
        return JSONToXMLResponse(
            xml_content=xml_content,
            status="success"
        )
    except (ValidationError, ProcessingError) as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/convert/from-yaml", response_model=YAMLToXMLResponse)
async def yaml_to_xml(request: YAMLToXMLRequest) -> YAMLToXMLResponse:
    """
    Convert YAML to XML
    
    - **yaml_content**: YAML string to convert
    - **root_tag**: Root element tag name
    - **pretty**: Format XML with indentation
    - **indent**: Number of spaces for indentation
    """
    try:
        converter = XMLConverter()
        xml_content = converter.yaml_to_xml(
            request.yaml_content,
            request.root_tag,
            request.pretty,
            request.indent
        )
        
        return YAMLToXMLResponse(
            xml_content=xml_content,
            status="success"
        )
    except (ValidationError, ProcessingError) as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Made with Bob
