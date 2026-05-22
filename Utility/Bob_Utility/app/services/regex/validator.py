"""
Regex Validator Service

Validates regex patterns and tests them against input strings.
"""

import re
from typing import List, Dict, Any, Optional
from app.core.logger import get_logger
from app.services.base import BaseService

logger = get_logger(__name__)


class RegexValidator(BaseService):
    """Service for validating regex patterns"""
    
    def __init__(self):
        super().__init__()
    
    def validate_pattern(self, pattern: str) -> Dict[str, Any]:
        """
        Validate a regex pattern
        
        Args:
            pattern: Regex pattern to validate
            
        Returns:
            Dictionary with validation results
        """
        try:
            result = {
                "pattern": pattern,
                "is_valid": False,
                "error": None,
                "flags_used": [],
                "groups_count": 0,
                "named_groups": [],
                "warnings": []
            }
            
            # Try to compile the pattern
            try:
                compiled = re.compile(pattern)
                result["is_valid"] = True
                
                # Extract pattern information
                result["groups_count"] = compiled.groups
                result["named_groups"] = list(compiled.groupindex.keys())
                
                # Check for common issues
                warnings = self._check_pattern_warnings(pattern)
                result["warnings"] = warnings
                
                logger.info(f"Pattern validated successfully: {pattern[:50]}...")
                
            except re.error as e:
                result["error"] = str(e)
                logger.warning(f"Invalid regex pattern: {str(e)}")
            
            return result
            
        except Exception as e:
            logger.error(f"Error validating pattern: {str(e)}")
            raise
    
    def _check_pattern_warnings(self, pattern: str) -> List[str]:
        """Check for common regex pattern issues"""
        warnings = []
        
        # Check for unescaped special characters
        if "." in pattern and r"\." not in pattern:
            if not any(x in pattern for x in [r".*", r".+", r".?"]):
                warnings.append("Unescaped '.' matches any character. Use '\\.' for literal dot.")
        
        # Check for catastrophic backtracking patterns
        if re.search(r'\([^)]*\+[^)]*\)\+', pattern):
            warnings.append("Potential catastrophic backtracking detected. Pattern may be slow on large inputs.")
        
        # Check for empty alternation
        if "||" in pattern:
            warnings.append("Empty alternation '||' detected. This may not work as expected.")
        
        # Check for unnecessary escaping
        unnecessarily_escaped = [r'\a', r'\b', r'\f', r'\n', r'\r', r'\t', r'\v']
        for esc in unnecessarily_escaped:
            if esc in pattern and not any(x in pattern for x in [r'\\', r'\x', r'\u']):
                warnings.append(f"'{esc}' is a special escape sequence. Use raw strings or double backslash if literal.")
        
        # Check for missing anchors
        if not pattern.startswith('^') and not pattern.endswith('$'):
            warnings.append("Pattern has no anchors (^ or $). It will match anywhere in the string.")
        
        # Check for overly broad patterns
        if pattern == ".*" or pattern == ".+":
            warnings.append("Pattern matches everything. Consider being more specific.")
        
        return warnings
    
    def test_pattern(
        self,
        pattern: str,
        test_strings: List[str],
        flags: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Test a regex pattern against multiple strings
        
        Args:
            pattern: Regex pattern to test
            test_strings: List of strings to test against
            flags: Optional list of regex flags ('IGNORECASE', 'MULTILINE', etc.)
            
        Returns:
            Dictionary with test results
        """
        try:
            # Validate pattern first
            validation = self.validate_pattern(pattern)
            if not validation["is_valid"]:
                return {
                    "pattern": pattern,
                    "is_valid": False,
                    "error": validation["error"],
                    "results": []
                }
            
            # Compile pattern with flags
            regex_flags = self._parse_flags(flags or [])
            compiled = re.compile(pattern, regex_flags)
            
            # Test against each string
            results = []
            for test_str in test_strings:
                match_result = self._test_single_string(compiled, test_str, pattern)
                results.append(match_result)
            
            # Calculate statistics
            matches_count = sum(1 for r in results if r["matched"])
            
            return {
                "pattern": pattern,
                "is_valid": True,
                "flags": flags or [],
                "total_tests": len(test_strings),
                "matches_count": matches_count,
                "match_rate": matches_count / len(test_strings) if test_strings else 0,
                "results": results
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
    
    def _test_single_string(
        self,
        compiled_pattern: re.Pattern,
        test_string: str,
        original_pattern: str
    ) -> Dict[str, Any]:
        """Test pattern against a single string"""
        result = {
            "test_string": test_string,
            "matched": False,
            "match_type": None,
            "matches": [],
            "groups": [],
            "named_groups": {}
        }
        
        # Try full match
        full_match = compiled_pattern.fullmatch(test_string)
        if full_match:
            result["matched"] = True
            result["match_type"] = "full"
            result["matches"] = [full_match.group(0)]
            result["groups"] = list(full_match.groups())
            result["named_groups"] = full_match.groupdict()
            return result
        
        # Try search (partial match)
        search_match = compiled_pattern.search(test_string)
        if search_match:
            result["matched"] = True
            result["match_type"] = "partial"
            result["matches"] = [search_match.group(0)]
            result["groups"] = list(search_match.groups())
            result["named_groups"] = search_match.groupdict()
            result["match_start"] = search_match.start()
            result["match_end"] = search_match.end()
            return result
        
        # Try findall (multiple matches)
        all_matches = compiled_pattern.findall(test_string)
        if all_matches:
            result["matched"] = True
            result["match_type"] = "multiple"
            result["matches"] = all_matches
            return result
        
        return result
    
    def find_all_matches(
        self,
        pattern: str,
        text: str,
        flags: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Find all matches of a pattern in text
        
        Args:
            pattern: Regex pattern
            text: Text to search in
            flags: Optional regex flags
            
        Returns:
            Dictionary with all matches and their positions
        """
        try:
            # Validate pattern
            validation = self.validate_pattern(pattern)
            if not validation["is_valid"]:
                return {
                    "pattern": pattern,
                    "is_valid": False,
                    "error": validation["error"],
                    "matches": []
                }
            
            # Compile with flags
            regex_flags = self._parse_flags(flags or [])
            compiled = re.compile(pattern, regex_flags)
            
            # Find all matches with positions
            matches = []
            for match in compiled.finditer(text):
                match_info = {
                    "match": match.group(0),
                    "start": match.start(),
                    "end": match.end(),
                    "groups": list(match.groups()),
                    "named_groups": match.groupdict()
                }
                matches.append(match_info)
            
            return {
                "pattern": pattern,
                "is_valid": True,
                "text_length": len(text),
                "matches_count": len(matches),
                "matches": matches
            }
            
        except Exception as e:
            logger.error(f"Error finding matches: {str(e)}")
            raise
    
    def replace_matches(
        self,
        pattern: str,
        text: str,
        replacement: str,
        flags: Optional[List[str]] = None,
        max_replacements: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Replace matches of a pattern in text
        
        Args:
            pattern: Regex pattern
            text: Text to search in
            replacement: Replacement string
            flags: Optional regex flags
            max_replacements: Maximum number of replacements (None for all)
            
        Returns:
            Dictionary with replacement results
        """
        try:
            # Validate pattern
            validation = self.validate_pattern(pattern)
            if not validation["is_valid"]:
                return {
                    "pattern": pattern,
                    "is_valid": False,
                    "error": validation["error"],
                    "result": text
                }
            
            # Compile with flags
            regex_flags = self._parse_flags(flags or [])
            compiled = re.compile(pattern, regex_flags)
            
            # Count matches before replacement
            matches_before = len(compiled.findall(text))
            
            # Perform replacement
            if max_replacements is not None:
                result_text = compiled.sub(replacement, text, count=max_replacements)
            else:
                result_text = compiled.sub(replacement, text)
            
            # Count matches after replacement
            matches_after = len(compiled.findall(result_text))
            replacements_made = matches_before - matches_after
            
            return {
                "pattern": pattern,
                "is_valid": True,
                "original_text": text,
                "result_text": result_text,
                "replacement": replacement,
                "matches_before": matches_before,
                "replacements_made": replacements_made,
                "matches_remaining": matches_after
            }
            
        except Exception as e:
            logger.error(f"Error replacing matches: {str(e)}")
            raise

# Made with Bob
