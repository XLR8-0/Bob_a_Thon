"""
Regex Assistant API Endpoints

Provides endpoints for regex pattern generation, validation, testing, and explanation.
"""

from fastapi import APIRouter, HTTPException, status
from app.api.v1.models import (
    RegexValidateRequest,
    RegexValidateResponse,
    RegexTestRequest,
    RegexTestResponse,
    RegexBatchTestRequest,
    RegexBatchTestResponse,
    RegexExplainRequest,
    RegexExplainResponse,
    RegexGenerateFromExamplesRequest,
    RegexGenerateFromExamplesResponse,
    RegexGenerateCustomRequest,
    RegexGenerateCustomResponse,
    RegexCommonPatternsResponse,
    RegexFindAllRequest,
    RegexFindAllResponse,
    RegexReplaceRequest,
    RegexReplaceResponse,
    RegexSplitRequest,
    RegexSplitResponse,
    RegexPerformanceTestRequest,
    RegexPerformanceTestResponse,
)
from app.services.regex.generator import RegexGenerator
from app.services.regex.validator import RegexValidator
from app.services.regex.explainer import RegexExplainer
from app.services.regex.tester import RegexTester
from app.core.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/regex", tags=["Regex Assistant"])

# Initialize services
generator = RegexGenerator()
validator = RegexValidator()
explainer = RegexExplainer()
tester = RegexTester()


@router.post("/validate", response_model=RegexValidateResponse)
async def validate_regex(request: RegexValidateRequest):
    """
    Validate a regex pattern
    
    Checks if the pattern is syntactically correct and provides warnings
    about potential issues.
    """
    try:
        result = validator.validate_pattern(request.pattern)
        return RegexValidateResponse(**result)
    except Exception as e:
        logger.error(f"Error validating regex: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error validating regex: {str(e)}"
        )


@router.post("/test", response_model=RegexTestResponse)
async def test_regex(request: RegexTestRequest):
    """
    Test a regex pattern against a string
    
    Supports different operations: search, match, fullmatch, findall, finditer
    """
    try:
        result = tester.test_pattern(
            pattern=request.pattern,
            test_string=request.test_string,
            flags=request.flags,
            operation=request.operation
        )
        return RegexTestResponse(**result)
    except Exception as e:
        logger.error(f"Error testing regex: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error testing regex: {str(e)}"
        )


@router.post("/test/batch", response_model=RegexBatchTestResponse)
async def batch_test_regex(request: RegexBatchTestRequest):
    """
    Test a regex pattern against multiple strings
    
    Returns statistics and individual results for each test string.
    """
    try:
        result = tester.batch_test(
            pattern=request.pattern,
            test_strings=request.test_strings,
            flags=request.flags,
            operation=request.operation
        )
        return RegexBatchTestResponse(**result)
    except Exception as e:
        logger.error(f"Error in batch test: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error in batch test: {str(e)}"
        )


@router.post("/explain", response_model=RegexExplainResponse)
async def explain_regex(request: RegexExplainRequest):
    """
    Explain a regex pattern in human-readable format
    
    Provides a summary, detailed breakdown, and complexity assessment.
    """
    try:
        result = explainer.explain_pattern(request.pattern)
        return RegexExplainResponse(**result)
    except Exception as e:
        logger.error(f"Error explaining regex: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error explaining regex: {str(e)}"
        )


@router.post("/generate/from-examples", response_model=RegexGenerateFromExamplesResponse)
async def generate_from_examples(request: RegexGenerateFromExamplesRequest):
    """
    Generate a regex pattern from example strings
    
    Analyzes the examples and creates a pattern that matches them.
    Optionally accepts a pattern_type hint (e.g., 'email', 'url') and
    allowed_chars (comma-separated special characters to allow).
    """
    try:
        result = generator.generate_from_examples(
            examples=request.examples,
            pattern_type=request.pattern_type,
            allowed_chars=request.allowed_chars,
            excluded_words=request.excluded_words
        )
        return RegexGenerateFromExamplesResponse(**result)
    except Exception as e:
        logger.error(f"Error generating regex from examples: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating regex: {str(e)}"
        )


@router.post("/generate/custom", response_model=RegexGenerateCustomResponse)
async def generate_custom_regex(request: RegexGenerateCustomRequest):
    """
    Generate a custom regex pattern based on requirements
    
    Requirements can include:
    - min_length, max_length
    - must_contain (list of character types)
    - must_start_with, must_end_with
    - allowed_chars
    """
    try:
        result = generator.generate_custom_pattern(request.requirements)
        return RegexGenerateCustomResponse(**result)
    except Exception as e:
        logger.error(f"Error generating custom regex: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating custom regex: {str(e)}"
        )


@router.get("/patterns/common", response_model=RegexCommonPatternsResponse)
async def get_common_patterns():
    """
    Get a list of common regex patterns
    
    Returns patterns for email, URL, phone numbers, dates, etc.
    """
    try:
        patterns = generator.list_common_patterns()
        return RegexCommonPatternsResponse(
            patterns=patterns,
            count=len(patterns)
        )
    except Exception as e:
        logger.error(f"Error getting common patterns: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting common patterns: {str(e)}"
        )


@router.get("/patterns/common/{pattern_type}")
async def get_common_pattern(pattern_type: str):
    """
    Get a specific common regex pattern by type
    
    Available types: email, url, phone_us, phone_international, ipv4, ipv6,
    date_iso, date_us, time_24h, time_12h, credit_card, ssn, zip_code,
    hex_color, username, password_strong, uuid, mac_address, domain, slug,
    html_tag, number_integer, number_decimal, number_positive, alphanumeric,
    letters_only, digits_only
    """
    try:
        pattern = generator.get_common_pattern(pattern_type)
        if pattern is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Pattern type '{pattern_type}' not found"
            )
        return {
            "pattern_type": pattern_type,
            "pattern": pattern
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting common pattern: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting common pattern: {str(e)}"
        )


@router.post("/find-all", response_model=RegexFindAllResponse)
async def find_all_matches(request: RegexFindAllRequest):
    """
    Find all matches of a pattern in text
    
    Returns all matches with their positions and captured groups.
    """
    try:
        result = validator.find_all_matches(
            pattern=request.pattern,
            text=request.text,
            flags=request.flags
        )
        return RegexFindAllResponse(**result)
    except Exception as e:
        logger.error(f"Error finding matches: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error finding matches: {str(e)}"
        )


@router.post("/replace", response_model=RegexReplaceResponse)
async def replace_matches(request: RegexReplaceRequest):
    """
    Replace matches of a pattern in text
    
    Replaces all or a specified number of matches with the replacement string.
    """
    try:
        result = validator.replace_matches(
            pattern=request.pattern,
            text=request.text,
            replacement=request.replacement,
            flags=request.flags,
            max_replacements=request.max_replacements
        )
        return RegexReplaceResponse(**result)
    except Exception as e:
        logger.error(f"Error replacing matches: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error replacing matches: {str(e)}"
        )


@router.post("/split", response_model=RegexSplitResponse)
async def split_text(request: RegexSplitRequest):
    """
    Split text using a regex pattern
    
    Splits the text at each match of the pattern.
    """
    try:
        result = tester.split_test(
            pattern=request.pattern,
            text=request.text,
            maxsplit=request.maxsplit,
            flags=request.flags
        )
        return RegexSplitResponse(**result)
    except Exception as e:
        logger.error(f"Error splitting text: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error splitting text: {str(e)}"
        )


@router.post("/performance", response_model=RegexPerformanceTestResponse)
async def test_performance(request: RegexPerformanceTestRequest):
    """
    Test regex pattern performance
    
    Runs the pattern multiple times and provides performance metrics.
    """
    try:
        result = tester.performance_test(
            pattern=request.pattern,
            text=request.text,
            iterations=request.iterations,
            flags=request.flags
        )
        return RegexPerformanceTestResponse(**result)
    except Exception as e:
        logger.error(f"Error testing performance: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error testing performance: {str(e)}"
        )

# Made with Bob
