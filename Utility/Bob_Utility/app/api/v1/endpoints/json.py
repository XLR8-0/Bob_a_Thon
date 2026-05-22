"""
JSON Toolkit API endpoints
"""

from fastapi import APIRouter, HTTPException

from app.api.v1.models import (
    JSONFormatRequest,
    JSONFormatResponse,
    JSONValidateRequest,
    JSONValidateResponse,
    JSONPathExecuteRequest,
    JSONPathExecuteResponse,
    JSONSchemaGenerateRequest,
    JSONSchemaGenerateResponse,
    JSONSchemaValidateRequest,
    JSONSchemaValidateResponse,
    JSONCompareRequest,
    JSONCompareResponse,
    JSONStructureRequest,
    JSONStructureResponse,
    JSONStatisticsRequest,
    JSONStatisticsResponse,
    JSONFlattenRequest,
    JSONFlattenResponse,
)
from app.core.exceptions import ValidationError, ProcessingError
from app.services.json import (
    JSONParser,
    JSONPathExecutor,
    JSONSchemaGenerator,
    JSONDiffer,
    JSONExplorer,
)

router = APIRouter(prefix="/json", tags=["JSON Toolkit"])


# Format & Validate Endpoints
@router.post("/format", response_model=JSONFormatResponse)
async def format_json(request: JSONFormatRequest) -> JSONFormatResponse:
    """
    Format and beautify JSON content
    
    - **json_content**: JSON string to format
    - **indent**: Number of spaces for indentation (0-8)
    - **sort_keys**: Sort object keys alphabetically
    - **ensure_ascii**: Escape non-ASCII characters
    """
    try:
        parser = JSONParser()
        formatted = parser.format(
            request.json_content,
            indent=request.indent,
            sort_keys=request.sort_keys,
            ensure_ascii=request.ensure_ascii
        )
        
        return JSONFormatResponse(
            formatted_json=formatted,
            status="success"
        )
    except (ValidationError, ProcessingError) as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/validate", response_model=JSONValidateResponse)
async def validate_json(request: JSONValidateRequest) -> JSONValidateResponse:
    """
    Validate JSON syntax
    
    - **json_content**: JSON string to validate
    """
    try:
        parser = JSONParser()
        is_valid = parser.validate(request.json_content)
        
        if is_valid:
            return JSONValidateResponse(
                is_valid=True,
                status="success"
            )
        else:
            return JSONValidateResponse(
                is_valid=False,
                status="success",
                error="JSON is not valid"
            )
    except Exception as e:
        return JSONValidateResponse(
            is_valid=False,
            status="success",
            error=str(e)
        )


@router.post("/minify")
async def minify_json(request: JSONFormatRequest):
    """
    Minify JSON by removing whitespace
    
    - **json_content**: JSON string to minify
    """
    try:
        parser = JSONParser()
        minified = parser.minify(request.json_content)
        
        return {
            "minified_json": minified,
            "status": "success"
        }
    except (ValidationError, ProcessingError) as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# JSONPath Endpoints
@router.post("/jsonpath/execute", response_model=JSONPathExecuteResponse)
async def execute_jsonpath(request: JSONPathExecuteRequest) -> JSONPathExecuteResponse:
    """
    Execute JSONPath query on JSON content
    
    - **json_content**: JSON string to query
    - **jsonpath_query**: JSONPath expression to execute
    - **use_extended**: Use extended JSONPath syntax
    """
    try:
        executor = JSONPathExecutor()
        matches = executor.execute_jsonpath(
            request.json_content,
            request.jsonpath_query,
            request.use_extended
        )
        
        return JSONPathExecuteResponse(
            matches=matches,
            match_count=len(matches),
            status="success"
        )
    except (ValidationError, ProcessingError) as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/jsonpath/find-key")
async def find_by_key(json_content: str, key_name: str, case_sensitive: bool = True):
    """
    Find all occurrences of a key in JSON
    
    - **json_content**: JSON string to search
    - **key_name**: Key name to search for
    - **case_sensitive**: Whether search is case-sensitive
    """
    try:
        executor = JSONPathExecutor()
        results = executor.find_by_key(json_content, key_name, case_sensitive)
        
        return {
            "results": results,
            "count": len(results),
            "status": "success"
        }
    except ProcessingError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Schema Endpoints
@router.post("/schema/generate", response_model=JSONSchemaGenerateResponse)
async def generate_schema(request: JSONSchemaGenerateRequest) -> JSONSchemaGenerateResponse:
    """
    Generate JSON schema from JSON data
    
    - **json_content**: JSON string to analyze
    - **title**: Optional schema title
    - **description**: Optional schema description
    """
    try:
        generator = JSONSchemaGenerator()
        schema = generator.generate_schema(
            request.json_content,
            request.title,
            request.description
        )
        
        return JSONSchemaGenerateResponse(
            schema=schema,
            status="success"
        )
    except (ValidationError, ProcessingError) as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/schema/validate", response_model=JSONSchemaValidateResponse)
async def validate_schema(request: JSONSchemaValidateRequest) -> JSONSchemaValidateResponse:
    """
    Validate JSON against a schema
    
    - **json_content**: JSON string to validate
    - **schema**: JSON schema dictionary
    """
    try:
        generator = JSONSchemaGenerator()
        result = generator.validate_against_schema(
            request.json_content,
            request.schema
        )
        
        return JSONSchemaValidateResponse(
            valid=result["valid"],
            error_count=result["error_count"],
            errors=result["errors"],
            status="success"
        )
    except ProcessingError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Comparison Endpoints
@router.post("/diff/compare", response_model=JSONCompareResponse)
async def compare_json(request: JSONCompareRequest) -> JSONCompareResponse:
    """
    Compare two JSON documents
    
    - **json1**: First JSON content
    - **json2**: Second JSON content
    - **ignore_order**: Ignore list order
    - **ignore_string_case**: Ignore string case differences
    """
    try:
        differ = JSONDiffer()
        result = differ.compare_json(
            request.json1,
            request.json2,
            request.ignore_order,
            request.ignore_string_case
        )
        
        return JSONCompareResponse(
            identical=result["identical"],
            differences=result["differences"],
            summary=result["summary"],
            status="success"
        )
    except (ValidationError, ProcessingError) as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Explorer Endpoints
@router.post("/explore/structure", response_model=JSONStructureResponse)
async def get_structure(request: JSONStructureRequest) -> JSONStructureResponse:
    """
    Get hierarchical structure of JSON document
    
    - **json_content**: JSON string to analyze
    - **max_depth**: Maximum depth to traverse
    """
    try:
        explorer = JSONExplorer()
        structure = explorer.get_structure(
            request.json_content,
            request.max_depth
        )
        
        return JSONStructureResponse(
            structure=structure,
            status="success"
        )
    except (ValidationError, ProcessingError) as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/explore/statistics", response_model=JSONStatisticsResponse)
async def get_statistics(request: JSONStatisticsRequest) -> JSONStatisticsResponse:
    """
    Get statistics about JSON document
    
    - **json_content**: JSON string to analyze
    """
    try:
        explorer = JSONExplorer()
        statistics = explorer.get_statistics(request.json_content)
        
        return JSONStatisticsResponse(
            statistics=statistics,
            status="success"
        )
    except ProcessingError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/flatten", response_model=JSONFlattenResponse)
async def flatten_json(request: JSONFlattenRequest) -> JSONFlattenResponse:
    """
    Flatten nested JSON structure
    
    - **json_content**: JSON string to flatten
    - **separator**: Key separator (default: ".")
    """
    try:
        explorer = JSONExplorer()
        flattened = explorer.flatten(
            request.json_content,
            request.separator
        )
        
        return JSONFlattenResponse(
            flattened=flattened,
            status="success"
        )
    except ProcessingError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Made with Bob