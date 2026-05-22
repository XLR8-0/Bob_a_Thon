"""
Regex Tester Service

Tests regex patterns with various options and provides detailed results.
"""

import re
import time
from typing import List, Dict, Any, Optional
from app.core.logger import get_logger
from app.services.base import BaseService

logger = get_logger(__name__)


class RegexTester(BaseService):
    """Service for testing regex patterns"""
    
    def __init__(self):
        super().__init__()
    
    def test_pattern(
        self,
        pattern: str,
        test_string: str,
        flags: Optional[List[str]] = None,
        operation: str = "search"
    ) -> Dict[str, Any]:
        """
        Test a regex pattern against a string
        
        Args:
            pattern: Regex pattern to test
            test_string: String to test against
            flags: Optional list of regex flags
            operation: Type of operation ('search', 'match', 'fullmatch', 'findall', 'finditer')
            
        Returns:
            Dictionary with test results
        """
        try:
            # Validate pattern
            try:
                regex_flags = self._parse_flags(flags or [])
                compiled = re.compile(pattern, regex_flags)
            except re.error as e:
                return {
                    "pattern": pattern,
                    "is_valid": False,
                    "error": str(e),
                    "result": None
                }
            
            # Measure execution time
            start_time = time.perf_counter()
            
            # Execute the requested operation
            if operation == "search":
                result = self._test_search(compiled, test_string)
            elif operation == "match":
                result = self._test_match(compiled, test_string)
            elif operation == "fullmatch":
                result = self._test_fullmatch(compiled, test_string)
            elif operation == "findall":
                result = self._test_findall(compiled, test_string)
            elif operation == "finditer":
                result = self._test_finditer(compiled, test_string)
            else:
                raise ValueError(f"Unknown operation: {operation}")
            
            execution_time = time.perf_counter() - start_time
            
            return {
                "pattern": pattern,
                "is_valid": True,
                "test_string": test_string,
                "operation": operation,
                "flags": flags or [],
                "execution_time_ms": round(execution_time * 1000, 3),
                "result": result
            }
            
        except Exception as e:
            logger.error(f"Error testing pattern: {str(e)}")
            raise
    
    def _parse_flags(self, flags: List[str]) -> int:
        """Parse string flags to regex flag constants"""
        flag_map = {
            "IGNORECASE": re.IGNORECASE,
            "I": re.IGNORECASE,
            "MULTILINE": re.MULTILINE,
            "M": re.MULTILINE,
            "DOTALL": re.DOTALL,
            "S": re.DOTALL,
            "VERBOSE": re.VERBOSE,
            "X": re.VERBOSE,
            "ASCII": re.ASCII,
            "A": re.ASCII,
        }
        
        result = 0
        for flag in flags:
            flag_upper = flag.upper()
            if flag_upper in flag_map:
                result |= flag_map[flag_upper]
        
        return result
    
    def _test_search(self, compiled: re.Pattern, text: str) -> Dict[str, Any]:
        """Test using search() - finds first match anywhere in string"""
        match = compiled.search(text)
        
        if match:
            return {
                "matched": True,
                "match": match.group(0),
                "start": match.start(),
                "end": match.end(),
                "groups": list(match.groups()),
                "named_groups": match.groupdict(),
                "span": match.span()
            }
        
        return {
            "matched": False,
            "match": None,
            "failure_reason": self._analyze_failure(compiled, text, "search")
        }
    
    def _test_match(self, compiled: re.Pattern, text: str) -> Dict[str, Any]:
        """Test using match() - matches at beginning of string"""
        match = compiled.match(text)
        
        if match:
            return {
                "matched": True,
                "match": match.group(0),
                "start": match.start(),
                "end": match.end(),
                "groups": list(match.groups()),
                "named_groups": match.groupdict(),
                "span": match.span()
            }
        
        return {
            "matched": False,
            "match": None,
            "failure_reason": self._analyze_failure(compiled, text, "match")
        }
    
    def _test_fullmatch(self, compiled: re.Pattern, text: str) -> Dict[str, Any]:
        """Test using fullmatch() - matches entire string"""
        match = compiled.fullmatch(text)
        
        if match:
            return {
                "matched": True,
                "match": match.group(0),
                "groups": list(match.groups()),
                "named_groups": match.groupdict()
            }
        
        return {
            "matched": False,
            "match": None,
            "failure_reason": self._analyze_failure(compiled, text, "fullmatch")
        }
    
    def _test_findall(self, compiled: re.Pattern, text: str) -> Dict[str, Any]:
        """Test using findall() - finds all non-overlapping matches"""
        matches = compiled.findall(text)
        
        return {
            "matched": len(matches) > 0,
            "matches_count": len(matches),
            "matches": matches
        }
    
    def _test_finditer(self, compiled: re.Pattern, text: str) -> Dict[str, Any]:
        """Test using finditer() - iterator over all matches"""
        matches = []
        
        for match in compiled.finditer(text):
            matches.append({
                "match": match.group(0),
                "start": match.start(),
                "end": match.end(),
                "groups": list(match.groups()),
                "named_groups": match.groupdict(),
                "span": match.span()
            })
        
        return {
            "matched": len(matches) > 0,
            "matches_count": len(matches),
            "matches": matches
        }
    
    def batch_test(
        self,
        pattern: str,
        test_strings: List[str],
        flags: Optional[List[str]] = None,
        operation: str = "search"
    ) -> Dict[str, Any]:
        """
        Test a pattern against multiple strings
        
        Args:
            pattern: Regex pattern to test
            test_strings: List of strings to test
            flags: Optional regex flags
            operation: Type of operation
            
        Returns:
            Dictionary with batch test results
        """
        try:
            results = []
            total_time = 0
            
            for test_str in test_strings:
                result = self.test_pattern(pattern, test_str, flags, operation)
                results.append(result)
                if result.get("execution_time_ms"):
                    total_time += result["execution_time_ms"]
            
            # Calculate statistics
            matched_count = sum(
                1 for r in results 
                if r.get("result", {}).get("matched", False)
            )
            
            return {
                "pattern": pattern,
                "operation": operation,
                "flags": flags or [],
                "total_tests": len(test_strings),
                "matched_count": matched_count,
                "match_rate": matched_count / len(test_strings) if test_strings else 0,
                "total_execution_time_ms": round(total_time, 3),
                "average_execution_time_ms": round(total_time / len(test_strings), 3) if test_strings else 0,
                "results": results
            }
            
        except Exception as e:
            logger.error(f"Error in batch test: {str(e)}")
            raise
    
    def split_test(
        self,
        pattern: str,
        text: str,
        maxsplit: int = 0,
        flags: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Test pattern splitting
        
        Args:
            pattern: Regex pattern to split on
            text: Text to split
            maxsplit: Maximum number of splits (0 = unlimited)
            flags: Optional regex flags
            
        Returns:
            Dictionary with split results
        """
        try:
            # Validate and compile pattern
            try:
                regex_flags = self._parse_flags(flags or [])
                compiled = re.compile(pattern, regex_flags)
            except re.error as e:
                return {
                    "pattern": pattern,
                    "is_valid": False,
                    "error": str(e),
                    "result": None
                }
            
            # Perform split
            start_time = time.perf_counter()
            parts = compiled.split(text, maxsplit=maxsplit)
            execution_time = time.perf_counter() - start_time
            
            return {
                "pattern": pattern,
                "is_valid": True,
                "text": text,
                "maxsplit": maxsplit,
                "flags": flags or [],
                "execution_time_ms": round(execution_time * 1000, 3),
                "parts_count": len(parts),
                "parts": parts
            }
            
        except Exception as e:
            logger.error(f"Error in split test: {str(e)}")
            raise
    
    def substitute_test(
        self,
        pattern: str,
        replacement: str,
        text: str,
        count: int = 0,
        flags: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Test pattern substitution
        
        Args:
            pattern: Regex pattern to match
            replacement: Replacement string
            text: Text to perform substitution on
            count: Maximum number of substitutions (0 = unlimited)
            flags: Optional regex flags
            
        Returns:
            Dictionary with substitution results
        """
        try:
            # Validate and compile pattern
            try:
                regex_flags = self._parse_flags(flags or [])
                compiled = re.compile(pattern, regex_flags)
            except re.error as e:
                return {
                    "pattern": pattern,
                    "is_valid": False,
                    "error": str(e),
                    "result": None
                }
            
            # Count matches before substitution
            matches_before = len(compiled.findall(text))
            
            # Perform substitution
            start_time = time.perf_counter()
            result_text = compiled.sub(replacement, text, count=count)
            execution_time = time.perf_counter() - start_time
            
            # Count matches after substitution
            matches_after = len(compiled.findall(result_text))
            
            return {
                "pattern": pattern,
                "is_valid": True,
                "original_text": text,
                "replacement": replacement,
                "result_text": result_text,
                "count": count,
                "flags": flags or [],
                "execution_time_ms": round(execution_time * 1000, 3),
                "matches_before": matches_before,
                "substitutions_made": matches_before - matches_after,
                "matches_after": matches_after,
                "text_changed": text != result_text
            }
            
        except Exception as e:
            logger.error(f"Error in substitute test: {str(e)}")
            raise
    
    def performance_test(
        self,
        pattern: str,
        text: str,
        iterations: int = 100,
        flags: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Test pattern performance
        
        Args:
            pattern: Regex pattern to test
            text: Text to test against
            iterations: Number of iterations to run
            flags: Optional regex flags
            
        Returns:
            Dictionary with performance metrics
        """
        try:
            # Validate and compile pattern
            try:
                regex_flags = self._parse_flags(flags or [])
                compiled = re.compile(pattern, regex_flags)
            except re.error as e:
                return {
                    "pattern": pattern,
                    "is_valid": False,
                    "error": str(e),
                    "result": None
                }
            
            # Run performance test
            times = []
            for _ in range(iterations):
                start_time = time.perf_counter()
                compiled.search(text)
                execution_time = time.perf_counter() - start_time
                times.append(execution_time * 1000)  # Convert to ms
            
            # Calculate statistics
            avg_time = sum(times) / len(times)
            min_time = min(times)
            max_time = max(times)
            
            return {
                "pattern": pattern,
                "is_valid": True,
                "text_length": len(text),
                "iterations": iterations,
                "flags": flags or [],
                "average_time_ms": round(avg_time, 3),
                "min_time_ms": round(min_time, 3),
                "max_time_ms": round(max_time, 3),
                "total_time_ms": round(sum(times), 3),
                "performance_rating": self._rate_performance(avg_time)
            }
            
        except Exception as e:
            logger.error(f"Error in performance test: {str(e)}")
            raise
    
    def _rate_performance(self, avg_time_ms: float) -> str:
        """Rate the performance based on average execution time"""
        if avg_time_ms < 0.1:
            return "excellent"
        elif avg_time_ms < 1:
            return "good"
        elif avg_time_ms < 10:
            return "acceptable"
        elif avg_time_ms < 100:
            return "slow"
        else:
            return "very_slow"
    
    def _analyze_failure(self, compiled: re.Pattern, text: str, operation: str) -> str:
        """
        Analyze why a pattern failed to match and provide detailed explanation
        
        Args:
            compiled: Compiled regex pattern
            text: Text that failed to match
            operation: Type of operation (search, match, fullmatch)
            
        Returns:
            Detailed explanation of why the match failed
        """
        pattern_str = compiled.pattern
        reasons = []
        
        # Check if pattern is too restrictive
        if operation == "match" and not text.startswith(pattern_str[:min(5, len(pattern_str))]):
            reasons.append(f"Pattern requires match at the START of string, but text starts with '{text[:20]}...'")
        
        if operation == "fullmatch":
            reasons.append(f"Pattern requires EXACT match of entire string. Text length: {len(text)}, Pattern may not match full length.")
        
        # Check for common issues
        if '^' in pattern_str and operation == "search":
            reasons.append("Pattern contains '^' (start anchor) which may be too restrictive for search operation")
        
        if '$' in pattern_str and operation == "search":
            reasons.append("Pattern contains '$' (end anchor) which may be too restrictive for search operation")
        
        # Check character classes
        if '\\d' in pattern_str and not any(c.isdigit() for c in text):
            reasons.append("Pattern expects digits (\\d) but text contains no digits")
        
        if '\\w' in pattern_str and not any(c.isalnum() or c == '_' for c in text):
            reasons.append("Pattern expects word characters (\\w) but text contains no alphanumeric characters")
        
        if '\\s' in pattern_str and not any(c.isspace() for c in text):
            reasons.append("Pattern expects whitespace (\\s) but text contains no whitespace")
        
        # Check for literal characters
        literals = re.findall(r'[a-zA-Z0-9]+', pattern_str)
        for literal in literals:
            if literal not in text:
                reasons.append(f"Pattern expects literal text '{literal}' which is not found in the input")
        
        # Check quantifiers
        if '+' in pattern_str:
            reasons.append("Pattern uses '+' quantifier (one or more) - ensure required characters appear at least once")
        
        if '*' in pattern_str:
            reasons.append("Pattern uses '*' quantifier (zero or more) - this is flexible but may not match as expected")
        
        if '{' in pattern_str:
            reasons.append("Pattern uses specific count quantifiers {n,m} - check if text has exact number of required characters")
        
        # Provide general advice
        if not reasons:
            reasons.append(f"Pattern structure doesn't match text structure. Try simplifying the pattern or checking for typos.")
            reasons.append(f"Text preview: '{text[:50]}{'...' if len(text) > 50 else ''}'")
        
        return " | ".join(reasons[:3])  # Return top 3 most relevant reasons

# Made with Bob
