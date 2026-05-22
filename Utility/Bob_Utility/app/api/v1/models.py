"""
Pydantic models for API requests and responses
"""

from typing import Any, Optional, List, Dict

from pydantic import BaseModel, Field


class XMLFormatRequest(BaseModel):
    """Request model for XML formatting"""

    xml_content: str = Field(..., description="XML content to format")
    indent: int = Field(2, ge=0, le=8, description="Indentation spaces")
    encoding: str = Field("utf-8", description="Output encoding")
    xml_declaration: bool = Field(True, description="Include XML declaration")


class XMLFormatResponse(BaseModel):
    """Response model for XML formatting"""

    formatted_xml: str = Field(..., description="Formatted XML content")
    status: str = Field("success", description="Operation status")
    line_count: Optional[int] = Field(None, description="Number of lines")


class XMLValidateRequest(BaseModel):
    """Request model for XML validation"""

    xml_content: str = Field(..., description="XML content to validate")


class XMLValidateResponse(BaseModel):
    """Response model for XML validation"""

    is_valid: bool = Field(..., description="Whether XML is valid")
    status: str = Field("success", description="Operation status")
    error: Optional[str] = Field(None, description="Error message if invalid")


class ErrorResponse(BaseModel):
    """Standard error response"""

    status: str = Field("error", description="Status")
    error_code: str = Field(..., description="Error code")
    message: str = Field(..., description="Error message")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional details")


# XPath Models
class XPathExecuteRequest(BaseModel):
    """Request model for XPath execution"""
    xml_content: str = Field(..., description="XML content to query")
    xpath_query: str = Field(..., description="XPath expression to execute")
    namespaces: Optional[Dict[str, str]] = Field(None, description="Namespace mappings")


class XPathExecuteResponse(BaseModel):
    """Response model for XPath execution"""
    matches: List[Dict[str, Any]] = Field(..., description="List of matching elements")
    match_count: int = Field(..., description="Number of matches found")
    status: str = Field("success", description="Operation status")


class XPathGenerateRequest(BaseModel):
    """Request model for XPath generation"""
    xml_content: str = Field(..., description="XML content")
    element_path: str = Field(..., description="Path to element")
    use_position: bool = Field(True, description="Include position predicates")
    use_attributes: bool = Field(False, description="Use attribute predicates")


class XPathGenerateResponse(BaseModel):
    """Response model for XPath generation"""
    xpath: str = Field(..., description="Generated XPath expression")
    status: str = Field("success", description="Operation status")


class XPathFindByValueRequest(BaseModel):
    """Request model for finding XPath by value"""
    xml_content: str = Field(..., description="XML content to search")
    search_value: str = Field(..., description="Value to search for")
    case_sensitive: bool = Field(False, description="Case-sensitive search")
    exact_match: bool = Field(False, description="Exact match or contains")


class XPathFindByValueResponse(BaseModel):
    """Response model for finding XPath by value"""
    matches: List[Dict[str, Any]] = Field(..., description="List of matching elements with XPath")
    match_count: int = Field(..., description="Number of matches found")
    status: str = Field("success", description="Operation status")


# Tree Explorer Models
class TreeStructureRequest(BaseModel):
    """Request model for tree structure"""
    xml_content: str = Field(..., description="XML content to analyze")
    max_depth: Optional[int] = Field(None, description="Maximum depth to traverse")
    include_attributes: bool = Field(True, description="Include element attributes")
    include_text: bool = Field(True, description="Include element text content")


class TreeStructureResponse(BaseModel):
    """Response model for tree structure"""
    tree: Dict[str, Any] = Field(..., description="Tree structure")
    status: str = Field("success", description="Operation status")


class TreeStatisticsRequest(BaseModel):
    """Request model for tree statistics"""
    xml_content: str = Field(..., description="XML content to analyze")


class TreeStatisticsResponse(BaseModel):
    """Response model for tree statistics"""
    statistics: Dict[str, Any] = Field(..., description="Tree statistics")
    status: str = Field("success", description="Operation status")


# XML Differ Models
class XMLCompareRequest(BaseModel):
    """Request model for XML comparison"""
    xml1: str = Field(..., description="First XML content")
    xml2: str = Field(..., description="Second XML content")
    ignore_order: bool = Field(False, description="Ignore element order")
    ignore_whitespace: bool = Field(True, description="Ignore whitespace differences")
    ignore_comments: bool = Field(True, description="Ignore XML comments")
    ignore_attributes: bool = Field(False, description="Ignore attribute differences")


class XMLCompareResponse(BaseModel):
    """Response model for XML comparison"""
    identical: bool = Field(..., description="Whether XMLs are identical")
    differences: List[Dict[str, Any]] = Field(..., description="List of differences")
    summary: Dict[str, int] = Field(..., description="Summary statistics")
    status: str = Field("success", description="Operation status")


# XSD Validator Models
class XSDValidateRequest(BaseModel):
    """Request model for XSD validation"""
    xml_content: str = Field(..., description="XML content to validate")
    xsd_content: str = Field(..., description="XSD schema content")
    cache_schema: bool = Field(True, description="Cache compiled schema")


class XSDValidateResponse(BaseModel):
    """Response model for XSD validation"""
    valid: bool = Field(..., description="Whether XML is valid")
    error_count: int = Field(..., description="Number of validation errors")
    errors: List[Dict[str, Any]] = Field(..., description="List of validation errors")
    status: str = Field("success", description="Operation status")


class XSDGenerateRequest(BaseModel):
    """Request model for XSD generation"""
    xml_content: str = Field(..., description="XML content to analyze")
    target_namespace: Optional[str] = Field(None, description="Target namespace for schema")


class XSDGenerateResponse(BaseModel):
    """Response model for XSD generation"""
    xsd_content: str = Field(..., description="Generated XSD schema")
    status: str = Field("success", description="Operation status")


# XML Converter Models
class XMLToJSONRequest(BaseModel):
    """Request model for XML to JSON conversion"""
    xml_content: str = Field(..., description="XML content to convert")
    pretty: bool = Field(True, description="Format JSON with indentation")
    indent: int = Field(2, ge=0, le=8, description="Indentation spaces")


class XMLToJSONResponse(BaseModel):
    """Response model for XML to JSON conversion"""
    json_content: str = Field(..., description="Converted JSON content")
    status: str = Field("success", description="Operation status")


class XMLToYAMLRequest(BaseModel):
    """Request model for XML to YAML conversion"""
    xml_content: str = Field(..., description="XML content to convert")
    default_flow_style: bool = Field(False, description="YAML flow style")


class XMLToYAMLResponse(BaseModel):
    """Response model for XML to YAML conversion"""
    yaml_content: str = Field(..., description="Converted YAML content")
    status: str = Field("success", description="Operation status")


class JSONToXMLRequest(BaseModel):
    """Request model for JSON to XML conversion"""
    json_content: str = Field(..., description="JSON content to convert")
    root_tag: str = Field("root", description="Root element tag name")
    pretty: bool = Field(True, description="Format XML with indentation")
    indent: int = Field(2, ge=0, le=8, description="Indentation spaces")


class JSONToXMLResponse(BaseModel):
    """Response model for JSON to XML conversion"""
    xml_content: str = Field(..., description="Converted XML content")
    status: str = Field("success", description="Operation status")


class YAMLToXMLRequest(BaseModel):
    """Request model for YAML to XML conversion"""
    yaml_content: str = Field(..., description="YAML content to convert")
    root_tag: str = Field("root", description="Root element tag name")
    pretty: bool = Field(True, description="Format XML with indentation")
    indent: int = Field(2, ge=0, le=8, description="Indentation spaces")


class YAMLToXMLResponse(BaseModel):
    """Response model for YAML to XML conversion"""
    xml_content: str = Field(..., description="Converted XML content")
    status: str = Field("success", description="Operation status")


# Made with Bob

# JSON Toolkit Models

class JSONFormatRequest(BaseModel):
    """Request model for JSON formatting"""
    json_content: str = Field(..., description="JSON content to format")
    indent: int = Field(2, ge=0, le=8, description="Indentation spaces")
    sort_keys: bool = Field(False, description="Sort object keys")
    ensure_ascii: bool = Field(False, description="Escape non-ASCII characters")


class JSONFormatResponse(BaseModel):
    """Response model for JSON formatting"""
    formatted_json: str = Field(..., description="Formatted JSON content")
    status: str = Field("success", description="Operation status")


class JSONValidateRequest(BaseModel):
    """Request model for JSON validation"""
    json_content: str = Field(..., description="JSON content to validate")


class JSONValidateResponse(BaseModel):
    """Response model for JSON validation"""
    is_valid: bool = Field(..., description="Whether JSON is valid")
    status: str = Field("success", description="Operation status")
    error: Optional[str] = Field(None, description="Error message if invalid")


class JSONPathExecuteRequest(BaseModel):
    """Request model for JSONPath execution"""
    json_content: str = Field(..., description="JSON content to query")
    jsonpath_query: str = Field(..., description="JSONPath expression")
    use_extended: bool = Field(True, description="Use extended JSONPath syntax")


class JSONPathExecuteResponse(BaseModel):
    """Response model for JSONPath execution"""
    matches: List[Dict[str, Any]] = Field(..., description="List of matches")
    match_count: int = Field(..., description="Number of matches")
    status: str = Field("success", description="Operation status")


class JSONSchemaGenerateRequest(BaseModel):
    """Request model for JSON schema generation"""
    json_content: str = Field(..., description="JSON content to analyze")
    title: Optional[str] = Field(None, description="Schema title")
    description: Optional[str] = Field(None, description="Schema description")


class JSONSchemaGenerateResponse(BaseModel):
    """Response model for JSON schema generation"""
    schema: Dict[str, Any] = Field(..., description="Generated JSON schema")
    status: str = Field("success", description="Operation status")


class JSONSchemaValidateRequest(BaseModel):
    """Request model for JSON schema validation"""
    json_content: str = Field(..., description="JSON content to validate")
    schema: Dict[str, Any] = Field(..., description="JSON schema")


class JSONSchemaValidateResponse(BaseModel):
    """Response model for JSON schema validation"""
    valid: bool = Field(..., description="Whether JSON is valid")
    error_count: int = Field(..., description="Number of errors")
    errors: List[Dict[str, Any]] = Field(..., description="Validation errors")
    status: str = Field("success", description="Operation status")


class JSONCompareRequest(BaseModel):
    """Request model for JSON comparison"""
    json1: str = Field(..., description="First JSON content")
    json2: str = Field(..., description="Second JSON content")
    ignore_order: bool = Field(False, description="Ignore list order")
    ignore_string_case: bool = Field(False, description="Ignore string case")


class JSONCompareResponse(BaseModel):
    """Response model for JSON comparison"""
    identical: bool = Field(..., description="Whether JSONs are identical")
    differences: List[Dict[str, Any]] = Field(..., description="List of differences")
    summary: Dict[str, int] = Field(..., description="Summary statistics")
    status: str = Field("success", description="Operation status")


class JSONStructureRequest(BaseModel):
    """Request model for JSON structure"""
    json_content: str = Field(..., description="JSON content to analyze")
    max_depth: Optional[int] = Field(None, description="Maximum depth")


class JSONStructureResponse(BaseModel):
    """Response model for JSON structure"""
    structure: Dict[str, Any] = Field(..., description="JSON structure")
    status: str = Field("success", description="Operation status")


class JSONStatisticsRequest(BaseModel):
    """Request model for JSON statistics"""
    json_content: str = Field(..., description="JSON content to analyze")


class JSONStatisticsResponse(BaseModel):
    """Response model for JSON statistics"""
    statistics: Dict[str, Any] = Field(..., description="JSON statistics")
    status: str = Field("success", description="Operation status")


class JSONFlattenRequest(BaseModel):
    """Request model for JSON flattening"""
    json_content: str = Field(..., description="JSON content to flatten")
    separator: str = Field(".", description="Key separator")


class JSONFlattenResponse(BaseModel):
    """Response model for JSON flattening"""
    flattened: Dict[str, Any] = Field(..., description="Flattened JSON")
    status: str = Field("success", description="Operation status")



# ============================================================================
# Regex Assistant Models
# ============================================================================

class RegexValidateRequest(BaseModel):
    """Request model for regex validation"""
    
    pattern: str = Field(..., description="Regex pattern to validate")


class RegexValidateResponse(BaseModel):
    """Response model for regex validation"""
    
    pattern: str = Field(..., description="The regex pattern")
    is_valid: bool = Field(..., description="Whether the pattern is valid")
    error: Optional[str] = Field(None, description="Error message if invalid")
    flags_used: List[str] = Field(default_factory=list, description="Flags used in pattern")
    groups_count: int = Field(0, description="Number of capturing groups")
    named_groups: List[str] = Field(default_factory=list, description="Named groups in pattern")
    warnings: List[str] = Field(default_factory=list, description="Pattern warnings")


class RegexTestRequest(BaseModel):
    """Request model for regex testing"""
    
    pattern: str = Field(..., description="Regex pattern to test")
    test_string: str = Field(..., description="String to test against")
    flags: Optional[List[str]] = Field(None, description="Regex flags (IGNORECASE, MULTILINE, etc.)")
    operation: str = Field("search", description="Operation type: search, match, fullmatch, findall, finditer")


class RegexTestResponse(BaseModel):
    """Response model for regex testing"""
    
    pattern: str = Field(..., description="The regex pattern")
    is_valid: bool = Field(..., description="Whether the pattern is valid")
    test_string: str = Field(..., description="The test string")
    operation: str = Field(..., description="Operation performed")
    flags: List[str] = Field(default_factory=list, description="Flags used")
    execution_time_ms: float = Field(..., description="Execution time in milliseconds")
    result: Dict[str, Any] = Field(..., description="Test result")
    error: Optional[str] = Field(None, description="Error message if invalid")


class RegexBatchTestRequest(BaseModel):
    """Request model for batch regex testing"""
    
    pattern: str = Field(..., description="Regex pattern to test")
    test_strings: List[str] = Field(..., description="List of strings to test")
    flags: Optional[List[str]] = Field(None, description="Regex flags")
    operation: str = Field("search", description="Operation type")


class RegexBatchTestResponse(BaseModel):
    """Response model for batch regex testing"""
    
    pattern: str = Field(..., description="The regex pattern")
    operation: str = Field(..., description="Operation performed")
    flags: List[str] = Field(default_factory=list, description="Flags used")
    total_tests: int = Field(..., description="Total number of tests")
    matched_count: int = Field(..., description="Number of matches")
    match_rate: float = Field(..., description="Match rate (0-1)")
    total_execution_time_ms: float = Field(..., description="Total execution time")
    average_execution_time_ms: float = Field(..., description="Average execution time")
    results: List[Dict[str, Any]] = Field(..., description="Individual test results")


class RegexExplainRequest(BaseModel):
    """Request model for regex explanation"""
    
    pattern: str = Field(..., description="Regex pattern to explain")


class RegexExplainResponse(BaseModel):
    """Response model for regex explanation"""
    
    pattern: str = Field(..., description="The regex pattern")
    is_valid: bool = Field(..., description="Whether the pattern is valid")
    summary: Optional[str] = Field(None, description="Human-readable summary")
    breakdown: Optional[List[Dict[str, Any]]] = Field(None, description="Detailed breakdown")
    complexity: Optional[str] = Field(None, description="Complexity level: low, medium, high")
    error: Optional[str] = Field(None, description="Error message if invalid")


class RegexGenerateFromExamplesRequest(BaseModel):
    """Request model for generating regex from examples"""
    
    examples: List[str] = Field(..., description="Example strings to match")
    pattern_type: Optional[str] = Field(None, description="Hint about pattern type (email, url, etc.)")
    allowed_chars: Optional[str] = Field(None, description="Comma-separated list of allowed special characters (e.g., '.,_-')")
    excluded_words: Optional[str] = Field(None, description="Comma-separated list of words to exclude (case-insensitive)")


class RegexGenerateFromExamplesResponse(BaseModel):
    """Response model for generating regex from examples"""
    
    pattern: str = Field(..., description="Generated regex pattern")
    pattern_type: str = Field(..., description="Pattern type")
    confidence: str = Field(..., description="Confidence level: low, medium, high")
    matches_all_examples: bool = Field(..., description="Whether pattern matches all examples")
    match_results: Optional[List[bool]] = Field(None, description="Match result for each example")
    source: str = Field(..., description="Source: common_pattern or generated")


class RegexGenerateCustomRequest(BaseModel):
    """Request model for generating custom regex"""
    
    requirements: Dict[str, Any] = Field(..., description="Pattern requirements")


class RegexGenerateCustomResponse(BaseModel):
    """Response model for generating custom regex"""
    
    pattern: str = Field(..., description="Generated regex pattern")
    requirements: Dict[str, Any] = Field(..., description="Requirements used")
    confidence: str = Field(..., description="Confidence level")
    source: str = Field(..., description="Source of pattern")


class RegexCommonPatternsResponse(BaseModel):
    """Response model for listing common patterns"""
    
    patterns: Dict[str, str] = Field(..., description="Dictionary of pattern types and patterns")
    count: int = Field(..., description="Number of patterns")


class RegexFindAllRequest(BaseModel):
    """Request model for finding all matches"""
    
    pattern: str = Field(..., description="Regex pattern")
    text: str = Field(..., description="Text to search in")
    flags: Optional[List[str]] = Field(None, description="Regex flags")


class RegexFindAllResponse(BaseModel):
    """Response model for finding all matches"""
    
    pattern: str = Field(..., description="The regex pattern")
    is_valid: bool = Field(..., description="Whether the pattern is valid")
    text_length: int = Field(..., description="Length of text")
    matches_count: int = Field(..., description="Number of matches found")
    matches: List[Dict[str, Any]] = Field(..., description="List of matches with positions")
    error: Optional[str] = Field(None, description="Error message if invalid")


class RegexReplaceRequest(BaseModel):
    """Request model for regex replacement"""
    
    pattern: str = Field(..., description="Regex pattern")
    text: str = Field(..., description="Text to search in")
    replacement: str = Field(..., description="Replacement string")
    flags: Optional[List[str]] = Field(None, description="Regex flags")
    max_replacements: Optional[int] = Field(None, description="Maximum replacements (None for all)")


class RegexReplaceResponse(BaseModel):
    """Response model for regex replacement"""
    
    pattern: str = Field(..., description="The regex pattern")
    is_valid: bool = Field(..., description="Whether the pattern is valid")
    original_text: str = Field(..., description="Original text")
    result_text: str = Field(..., description="Text after replacement")
    replacement: str = Field(..., description="Replacement string used")
    matches_before: int = Field(..., description="Matches before replacement")
    replacements_made: int = Field(..., description="Number of replacements made")
    matches_remaining: int = Field(..., description="Matches remaining after replacement")
    error: Optional[str] = Field(None, description="Error message if invalid")


class RegexSplitRequest(BaseModel):
    """Request model for regex split"""
    
    pattern: str = Field(..., description="Regex pattern to split on")
    text: str = Field(..., description="Text to split")
    maxsplit: int = Field(0, description="Maximum splits (0 for unlimited)")
    flags: Optional[List[str]] = Field(None, description="Regex flags")


class RegexSplitResponse(BaseModel):
    """Response model for regex split"""
    
    pattern: str = Field(..., description="The regex pattern")
    is_valid: bool = Field(..., description="Whether the pattern is valid")
    text: str = Field(..., description="Original text")
    maxsplit: int = Field(..., description="Maximum splits")
    flags: List[str] = Field(default_factory=list, description="Flags used")
    execution_time_ms: float = Field(..., description="Execution time")
    parts_count: int = Field(..., description="Number of parts after split")
    parts: List[str] = Field(..., description="Split parts")
    error: Optional[str] = Field(None, description="Error message if invalid")


class RegexPerformanceTestRequest(BaseModel):
    """Request model for regex performance testing"""
    
    pattern: str = Field(..., description="Regex pattern to test")
    text: str = Field(..., description="Text to test against")
    iterations: int = Field(100, ge=1, le=10000, description="Number of iterations")
    flags: Optional[List[str]] = Field(None, description="Regex flags")


class RegexPerformanceTestResponse(BaseModel):
    """Response model for regex performance testing"""
    
    pattern: str = Field(..., description="The regex pattern")
    is_valid: bool = Field(..., description="Whether the pattern is valid")
    text_length: int = Field(..., description="Length of test text")
    iterations: int = Field(..., description="Number of iterations")
    flags: List[str] = Field(default_factory=list, description="Flags used")
    average_time_ms: float = Field(..., description="Average execution time")
    min_time_ms: float = Field(..., description="Minimum execution time")
    max_time_ms: float = Field(..., description="Maximum execution time")
    total_time_ms: float = Field(..., description="Total execution time")
    performance_rating: str = Field(..., description="Performance rating")
    error: Optional[str] = Field(None, description="Error message if invalid")
