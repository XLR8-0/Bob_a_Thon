"""
Regex Explainer Service

Explains regex patterns in human-readable format.
"""

import re
from typing import List, Dict, Any, Optional
from app.core.logger import get_logger
from app.services.base import BaseService

logger = get_logger(__name__)


class RegexExplainer(BaseService):
    """Service for explaining regex patterns"""
    
    def __init__(self):
        super().__init__()
        
        # Character class explanations
        self.char_classes = {
            r"\d": "any digit (0-9)",
            r"\D": "any non-digit",
            r"\w": "any word character (letter, digit, or underscore)",
            r"\W": "any non-word character",
            r"\s": "any whitespace character (space, tab, newline)",
            r"\S": "any non-whitespace character",
            r".": "any character except newline",
            r"\b": "word boundary",
            r"\B": "non-word boundary",
            r"\A": "start of string",
            r"\Z": "end of string",
            r"\n": "newline character",
            r"\r": "carriage return",
            r"\t": "tab character",
            r"\f": "form feed",
            r"\v": "vertical tab",
        }
        
        # Quantifier explanations
        self.quantifiers = {
            "*": "0 or more times",
            "+": "1 or more times",
            "?": "0 or 1 time (optional)",
            "{n}": "exactly n times",
            "{n,}": "n or more times",
            "{n,m}": "between n and m times",
        }
    
    def explain_pattern(self, pattern: str) -> Dict[str, Any]:
        """
        Explain a regex pattern in human-readable format
        
        Args:
            pattern: Regex pattern to explain
            
        Returns:
            Dictionary with explanation and breakdown
        """
        try:
            # Validate pattern first
            try:
                re.compile(pattern)
            except re.error as e:
                return {
                    "pattern": pattern,
                    "is_valid": False,
                    "error": str(e),
                    "explanation": None
                }
            
            # Parse and explain the pattern
            explanation = self._parse_pattern(pattern)
            
            # Generate summary
            summary = self._generate_summary(pattern, explanation)
            
            return {
                "pattern": pattern,
                "is_valid": True,
                "summary": summary,
                "breakdown": explanation,
                "complexity": self._assess_complexity(pattern)
            }
            
        except Exception as e:
            logger.error(f"Error explaining pattern: {str(e)}")
            raise
    
    def _parse_pattern(self, pattern: str) -> List[Dict[str, Any]]:
        """Parse pattern into explainable components"""
        components = []
        i = 0
        
        while i < len(pattern):
            char = pattern[i]
            
            # Anchors
            if char == '^':
                components.append({
                    "token": "^",
                    "type": "anchor",
                    "explanation": "Start of string/line"
                })
                i += 1
            
            elif char == '$':
                components.append({
                    "token": "$",
                    "type": "anchor",
                    "explanation": "End of string/line"
                })
                i += 1
            
            # Escape sequences
            elif char == '\\' and i + 1 < len(pattern):
                escape_seq = pattern[i:i+2]
                explanation = self.char_classes.get(escape_seq, f"Escaped character: {escape_seq}")
                components.append({
                    "token": escape_seq,
                    "type": "escape",
                    "explanation": explanation
                })
                i += 2
            
            # Character classes
            elif char == '[':
                end = pattern.find(']', i)
                if end != -1:
                    char_class = pattern[i:end+1]
                    components.append({
                        "token": char_class,
                        "type": "character_class",
                        "explanation": self._explain_char_class(char_class)
                    })
                    i = end + 1
                else:
                    components.append({
                        "token": char,
                        "type": "literal",
                        "explanation": f"Literal character: {char}"
                    })
                    i += 1
            
            # Groups
            elif char == '(':
                # Find matching closing parenthesis
                depth = 1
                end = i + 1
                while end < len(pattern) and depth > 0:
                    if pattern[end] == '(' and (end == 0 or pattern[end-1] != '\\'):
                        depth += 1
                    elif pattern[end] == ')' and (end == 0 or pattern[end-1] != '\\'):
                        depth -= 1
                    end += 1
                
                if depth == 0:
                    group = pattern[i:end]
                    components.append({
                        "token": group,
                        "type": "group",
                        "explanation": self._explain_group(group)
                    })
                    i = end
                else:
                    components.append({
                        "token": char,
                        "type": "literal",
                        "explanation": f"Literal character: {char}"
                    })
                    i += 1
            
            # Quantifiers
            elif char in '*+?':
                if components:
                    last = components[-1]
                    last["quantifier"] = char
                    last["explanation"] += f" (repeated {self.quantifiers[char]})"
                i += 1
            
            elif char == '{':
                end = pattern.find('}', i)
                if end != -1:
                    quantifier = pattern[i:end+1]
                    if components:
                        last = components[-1]
                        last["quantifier"] = quantifier
                        last["explanation"] += f" (repeated {self._explain_quantifier(quantifier)})"
                    i = end + 1
                else:
                    components.append({
                        "token": char,
                        "type": "literal",
                        "explanation": f"Literal character: {char}"
                    })
                    i += 1
            
            # Alternation
            elif char == '|':
                components.append({
                    "token": "|",
                    "type": "alternation",
                    "explanation": "OR (matches either the pattern before or after)"
                })
                i += 1
            
            # Dot (any character)
            elif char == '.':
                components.append({
                    "token": ".",
                    "type": "wildcard",
                    "explanation": "Any character (except newline)"
                })
                i += 1
            
            # Literal characters
            else:
                components.append({
                    "token": char,
                    "type": "literal",
                    "explanation": f"Literal character: '{char}'"
                })
                i += 1
        
        return components
    
    def _explain_char_class(self, char_class: str) -> str:
        """Explain a character class like [a-z] or [^0-9]"""
        content = char_class[1:-1]  # Remove [ and ]
        
        if content.startswith('^'):
            return f"Any character NOT in: {content[1:]}"
        
        # Check for ranges
        if '-' in content and len(content) >= 3:
            parts = []
            i = 0
            while i < len(content):
                if i + 2 < len(content) and content[i+1] == '-':
                    parts.append(f"{content[i]} through {content[i+2]}")
                    i += 3
                else:
                    parts.append(f"'{content[i]}'")
                    i += 1
            return f"Any character in: {', '.join(parts)}"
        
        return f"Any character in: {content}"
    
    def _explain_group(self, group: str) -> str:
        """Explain a group like (abc) or (?:abc) or (?P<name>abc)"""
        content = group[1:-1]  # Remove ( and )
        
        # Non-capturing group
        if content.startswith('?:'):
            return f"Non-capturing group: {content[2:]}"
        
        # Named group
        if content.startswith('?P<'):
            end = content.find('>')
            if end != -1:
                name = content[3:end]
                pattern = content[end+1:]
                return f"Named group '{name}': {pattern}"
        
        # Lookahead
        if content.startswith('?='):
            return f"Positive lookahead: {content[2:]}"
        
        if content.startswith('?!'):
            return f"Negative lookahead: {content[2:]}"
        
        # Lookbehind
        if content.startswith('?<='):
            return f"Positive lookbehind: {content[3:]}"
        
        if content.startswith('?<!'):
            return f"Negative lookbehind: {content[3:]}"
        
        # Capturing group
        return f"Capturing group: {content}"
    
    def _explain_quantifier(self, quantifier: str) -> str:
        """Explain a quantifier like {3} or {2,5}"""
        content = quantifier[1:-1]  # Remove { and }
        
        if ',' not in content:
            return f"exactly {content} times"
        
        parts = content.split(',')
        if len(parts) == 2:
            if parts[1]:
                return f"between {parts[0]} and {parts[1]} times"
            else:
                return f"{parts[0]} or more times"
        
        return content
    
    def _generate_summary(self, pattern: str, components: List[Dict[str, Any]]) -> str:
        """Generate a human-readable summary of the pattern"""
        parts = []
        
        # Check for anchors
        has_start_anchor = pattern.startswith('^')
        has_end_anchor = pattern.endswith('$')
        
        if has_start_anchor and has_end_anchor:
            parts.append("Match the entire string that")
        elif has_start_anchor:
            parts.append("Match from the start of the string")
        elif has_end_anchor:
            parts.append("Match up to the end of the string")
        else:
            parts.append("Match anywhere in the string")
        
        # Analyze main pattern
        non_anchor_components = [
            c for c in components 
            if c["type"] not in ["anchor"]
        ]
        
        if len(non_anchor_components) == 0:
            parts.append("(empty pattern)")
        elif len(non_anchor_components) == 1:
            parts.append(f"contains: {non_anchor_components[0]['explanation']}")
        else:
            parts.append("contains:")
            for comp in non_anchor_components[:3]:  # Show first 3 components
                parts.append(f"  - {comp['explanation']}")
            if len(non_anchor_components) > 3:
                parts.append(f"  ... and {len(non_anchor_components) - 3} more components")
        
        return " ".join(parts)
    
    def _assess_complexity(self, pattern: str) -> str:
        """Assess the complexity of a regex pattern"""
        score = 0
        
        # Length
        if len(pattern) > 50:
            score += 2
        elif len(pattern) > 20:
            score += 1
        
        # Nested groups
        max_depth = 0
        current_depth = 0
        for char in pattern:
            if char == '(':
                current_depth += 1
                max_depth = max(max_depth, current_depth)
            elif char == ')':
                current_depth -= 1
        
        if max_depth > 3:
            score += 2
        elif max_depth > 1:
            score += 1
        
        # Lookaheads/lookbehinds
        if '?=' in pattern or '?!' in pattern or '?<=' in pattern or '?<!' in pattern:
            score += 2
        
        # Backreferences
        if re.search(r'\\[1-9]', pattern):
            score += 1
        
        # Quantifiers
        quantifier_count = pattern.count('*') + pattern.count('+') + pattern.count('?')
        if quantifier_count > 5:
            score += 2
        elif quantifier_count > 2:
            score += 1
        
        # Determine complexity level
        if score >= 6:
            return "high"
        elif score >= 3:
            return "medium"
        else:
            return "low"
    
    def get_examples(self, pattern: str, count: int = 5) -> Dict[str, Any]:
        """
        Generate example strings that would match the pattern
        
        Args:
            pattern: Regex pattern
            count: Number of examples to generate
            
        Returns:
            Dictionary with example strings
        """
        try:
            # Validate pattern
            try:
                re.compile(pattern)
            except re.error as e:
                return {
                    "pattern": pattern,
                    "is_valid": False,
                    "error": str(e),
                    "examples": []
                }
            
            # Generate examples (simplified version)
            examples = self._generate_examples(pattern, count)
            
            return {
                "pattern": pattern,
                "is_valid": True,
                "examples": examples,
                "note": "These are simplified examples. Actual matches may vary."
            }
            
        except Exception as e:
            logger.error(f"Error generating examples: {str(e)}")
            raise
    
    def _generate_examples(self, pattern: str, count: int) -> List[str]:
        """Generate example strings (simplified implementation)"""
        examples = []
        
        # Remove anchors for example generation
        clean_pattern = pattern.replace('^', '').replace('$', '')
        
        # Very basic example generation
        # In a production system, you'd want a more sophisticated approach
        
        if r'\d' in clean_pattern:
            examples.append(clean_pattern.replace(r'\d', '5'))
        
        if r'\w' in clean_pattern:
            examples.append(clean_pattern.replace(r'\w', 'a'))
        
        if r'\s' in clean_pattern:
            examples.append(clean_pattern.replace(r'\s', ' '))
        
        if '.' in clean_pattern:
            examples.append(clean_pattern.replace('.', 'x'))
        
        # Add a generic example
        if not examples:
            examples.append("example_string")
        
        return examples[:count]

# Made with Bob
