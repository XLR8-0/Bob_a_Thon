"""
Regex Generator Service

Generates regex patterns based on user requirements and examples.
"""

import re
from typing import List, Dict, Any, Optional
from app.core.logger import get_logger
from app.services.base import BaseService

logger = get_logger(__name__)


class RegexGenerator(BaseService):
    """Service for generating regex patterns"""
    
    def __init__(self):
        super().__init__()
        self.common_patterns = {
            "email": r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
            "url": r"^https?://(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&/=]*)$",
            "phone_us": r"^(\+1[-.\s]?)?(\(?\d{3}\)?[-.\s]?)?\d{3}[-.\s]?\d{4}$",
            "phone_international": r"^\+?[1-9]\d{1,14}$",
            "ipv4": r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$",
            "ipv6": r"^(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}$",
            "date_iso": r"^\d{4}-\d{2}-\d{2}$",
            "date_us": r"^(0?[1-9]|1[0-2])/(0?[1-9]|[12][0-9]|3[01])/\d{4}$",
            "time_24h": r"^([01]?[0-9]|2[0-3]):[0-5][0-9](?::[0-5][0-9])?$",
            "time_12h": r"^(0?[1-9]|1[0-2]):[0-5][0-9](?::[0-5][0-9])?\s?[AaPp][Mm]$",
            "credit_card": r"^(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|3[47][0-9]{13}|3(?:0[0-5]|[68][0-9])[0-9]{11}|6(?:011|5[0-9]{2})[0-9]{12}|(?:2131|1800|35\d{3})\d{11})$",
            "ssn": r"^\d{3}-\d{2}-\d{4}$",
            "zip_code": r"^\d{5}(?:-\d{4})?$",
            "hex_color": r"^#?([a-fA-F0-9]{6}|[a-fA-F0-9]{3})$",
            "username": r"^[a-zA-Z0-9_-]{3,16}$",
            "password_strong": r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$",
            "uuid": r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$",
            "mac_address": r"^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$",
            "domain": r"^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$",
            "slug": r"^[a-z0-9]+(?:-[a-z0-9]+)*$",
            "html_tag": r"<([a-z]+)([^<]+)*(?:>(.*)<\/\1>|\s+\/>)",
            "number_integer": r"^-?\d+$",
            "number_decimal": r"^-?\d+\.?\d*$",
            "number_positive": r"^\d+\.?\d*$",
            "alphanumeric": r"^[a-zA-Z0-9]+$",
            "letters_only": r"^[a-zA-Z]+$",
            "digits_only": r"^\d+$",
        }
    
    def get_common_pattern(self, pattern_type: str) -> Optional[str]:
        """
        Get a common regex pattern by type
        
        Args:
            pattern_type: Type of pattern (e.g., 'email', 'url', 'phone_us')
            
        Returns:
            Regex pattern string or None if not found
        """
        try:
            pattern = self.common_patterns.get(pattern_type.lower())
            if pattern:
                logger.info(f"Retrieved common pattern: {pattern_type}")
            else:
                logger.warning(f"Pattern type not found: {pattern_type}")
            return pattern
        except Exception as e:
            logger.error(f"Error getting common pattern: {str(e)}")
            raise
    
    def list_common_patterns(self) -> Dict[str, str]:
        """
        List all available common patterns
        
        Returns:
            Dictionary of pattern types and their regex patterns
        """
        return self.common_patterns.copy()
    
    def _add_excluded_words(self, pattern: str, excluded_words: str) -> str:
        """
        Add negative lookahead to exclude strings containing specific words (case-insensitive).
        
        Args:
            pattern: Original regex pattern
            excluded_words: Comma-separated list of words to exclude
            
        Returns:
            Pattern with negative lookahead added
        """
        if not excluded_words:
            return pattern
        
        # Parse excluded words
        words = [w.strip() for w in excluded_words.split(',') if w.strip()]
        if not words:
            return pattern
        
        # Build negative lookahead for each word (case-insensitive)
        # Format: (?i:(?!.*word1))(?i:(?!.*word2))...pattern
        # This checks if the word appears anywhere in the string (case-insensitive)
        lookaheads = []
        for word in words:
            # Escape special regex characters in the word
            escaped_word = re.escape(word)
            # Create case-insensitive negative lookahead that checks anywhere in string
            # (?i:...) makes the lookahead case-insensitive
            lookaheads.append(f"(?i:(?!.*{escaped_word}))")
        
        # Combine all lookaheads and prepend to pattern
        # Remove ^ from original pattern if present
        if pattern.startswith('^'):
            pattern = pattern[1:]
        
        return '^' + ''.join(lookaheads) + pattern
    
    def _parse_allowed_chars(self, allowed_chars: Optional[str]) -> set:
        """
        Parse allowed characters from input string.
        Handles both single characters and comma-separated values.
        Examples: "." -> {'.'}
                  ".,_" -> {'.', '_'}
                  "., _" -> {'.', '_'}
        """
        if not allowed_chars:
            return set()
        
        # If there's a comma, split by comma
        if ',' in allowed_chars:
            return set(c.strip() for c in allowed_chars.split(',') if c.strip())
        else:
            # Single character or multiple characters without comma
            # Treat each character as separate
            return set(c for c in allowed_chars.strip() if c and not c.isspace())
    
    def generate_from_examples(
        self,
        examples: List[str],
        pattern_type: Optional[str] = None,
        allowed_chars: Optional[str] = None,
        excluded_words: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate regex pattern from example strings
        
        Args:
            examples: List of example strings to match
            pattern_type: Optional hint about the pattern type
            allowed_chars: Optional comma-separated list of allowed special characters
            excluded_words: Optional comma-separated list of words to exclude (case-insensitive)
            
        Returns:
            Dictionary with generated pattern and metadata
        """
        try:
            if not examples:
                raise ValueError("At least one example is required")
            
            # If pattern type is provided, try to use common pattern
            if pattern_type:
                common_pattern = self.get_common_pattern(pattern_type)
                if common_pattern:
                    # Test if common pattern matches all examples
                    if all(re.match(common_pattern, ex) for ex in examples):
                        return {
                            "pattern": common_pattern,
                            "pattern_type": pattern_type,
                            "confidence": "high",
                            "matches_all_examples": True,
                            "source": "common_pattern"
                        }
            
            # Analyze examples to generate pattern
            pattern = self._analyze_and_generate(examples, allowed_chars)
            
            # Add negative lookahead for excluded words if specified
            if excluded_words:
                pattern = self._add_excluded_words(pattern, excluded_words)
            
            # Test generated pattern
            matches = [bool(re.match(pattern, ex)) for ex in examples]
            matches_all = all(matches)
            
            return {
                "pattern": pattern,
                "pattern_type": pattern_type or "custom",
                "confidence": "high" if matches_all else "medium",
                "matches_all_examples": matches_all,
                "match_results": matches,
                "source": "generated"
            }
            
        except Exception as e:
            logger.error(f"Error generating pattern from examples: {str(e)}")
            raise
    
    def _analyze_and_generate(self, examples: List[str], allowed_chars: Optional[str] = None) -> str:
        """
        Analyze examples and generate a regex pattern
        
        Args:
            examples: List of example strings
            allowed_chars: Optional comma-separated list of allowed special characters
            
        Returns:
            Generated regex pattern
        """
        if len(examples) == 1:
            # For single example, create a literal pattern with some flexibility
            return self._generate_flexible_pattern(examples[0])
        
        # Try to detect structured patterns (like phone numbers, dates, etc.)
        structured_pattern = self._detect_structured_pattern(examples, allowed_chars)
        if structured_pattern:
            return structured_pattern
        
        # Try character-type based pattern (for cases with optional separators)
        char_type_pattern = self._generate_char_type_pattern(examples, allowed_chars)
        if char_type_pattern:
            return char_type_pattern
        
        # Find common structure
        min_len = min(len(ex) for ex in examples)
        max_len = max(len(ex) for ex in examples)
        
        # Check if all examples have same length
        same_length = min_len == max_len
        
        # Analyze character types at each position
        pattern_parts = []
        
        if same_length:
            # Position-based analysis for same-length strings
            for i in range(min_len):
                chars = [ex[i] for ex in examples]
                pattern_parts.append(self._get_char_class(chars))
            pattern = "^" + "".join(pattern_parts) + "$"
        else:
            # Length-flexible pattern - improved logic
            # Find common prefix
            common_prefix_len = self._find_common_prefix_length(examples)
            
            # Find common suffix
            common_suffix_len = self._find_common_suffix_length(examples)
            
            # Build pattern with three parts: prefix, middle, suffix
            if common_prefix_len > 0:
                # Add exact prefix pattern
                for i in range(common_prefix_len):
                    chars = [ex[i] for ex in examples]
                    pattern_parts.append(self._get_char_class(chars))
            
            # Middle part - analyze the variable section
            middle_start = common_prefix_len
            middle_end = min_len - common_suffix_len if common_suffix_len > 0 else min_len
            
            if middle_end > middle_start:
                # Analyze middle section character types
                middle_chars = []
                for ex in examples:
                    middle_section = ex[middle_start:len(ex)-common_suffix_len if common_suffix_len > 0 else len(ex)]
                    middle_chars.extend(middle_section)
                
                # Determine character class for middle section
                if all(c.isdigit() for c in middle_chars):
                    pattern_parts.append(r"\d+")
                elif all(c.isalpha() for c in middle_chars):
                    if all(c.isupper() for c in middle_chars):
                        pattern_parts.append(r"[A-Z]+")
                    elif all(c.islower() for c in middle_chars):
                        pattern_parts.append(r"[a-z]+")
                    else:
                        pattern_parts.append(r"[a-zA-Z]+")
                elif all(c.isalnum() for c in middle_chars):
                    pattern_parts.append(r"\w+")
                else:
                    # Mixed characters - be more specific
                    unique_chars = set(middle_chars)
                    if len(unique_chars) <= 10:
                        escaped = [re.escape(c) for c in unique_chars]
                        pattern_parts.append(f"[{''.join(escaped)}]+")
                    else:
                        pattern_parts.append(r".+")
            
            # Add suffix pattern
            if common_suffix_len > 0:
                for i in range(common_suffix_len):
                    chars = [ex[-(common_suffix_len-i)] for ex in examples]
                    pattern_parts.append(self._get_char_class(chars))
            
            pattern = "^" + "".join(pattern_parts) + "$"
        
        return pattern
    
    def _detect_structured_pattern(self, examples: List[str], allowed_chars: Optional[str] = None) -> Optional[str]:
        """
        Detect structured patterns like phone numbers, dates, etc.
        Returns a regex pattern if a structure is detected, None otherwise.
        
        Args:
            examples: List of example strings
            allowed_chars: Optional comma-separated list of allowed special characters
        """
        if not examples:
            return None
        
        # Tokenize each example into segments of digits, letters, and separators
        tokenized = []
        for example in examples:
            tokens = []
            i = 0
            while i < len(example):
                char = example[i]
                if char.isdigit():
                    # Collect consecutive digits
                    count = 1
                    while i + count < len(example) and example[i + count].isdigit():
                        count += 1
                    tokens.append(('digit', count))
                    i += count
                elif char.isalpha():
                    # Collect consecutive letters
                    count = 1
                    while i + count < len(example) and example[i + count].isalpha():
                        count += 1
                    tokens.append(('alpha', count))
                    i += count
                else:
                    # Separator or special character
                    tokens.append(('sep', char))
                    i += 1
            tokenized.append(tokens)
        
        # Normalize by merging consecutive separators
        normalized = []
        for tokens in tokenized:
            norm_tokens = []
            i = 0
            while i < len(tokens):
                if tokens[i][0] == 'sep':
                    # Collect all consecutive separators
                    seps = []
                    while i < len(tokens) and tokens[i][0] == 'sep':
                        seps.append(tokens[i][1])
                        i += 1
                    # Add as single merged separator token
                    norm_tokens.append(('sep', ''.join(seps)))
                else:
                    norm_tokens.append(tokens[i])
                    i += 1
            normalized.append(norm_tokens)
        
        # Check if all examples have similar token structure
        structure_info = self._analyze_structure_similarity(normalized)
        if not structure_info:
            return None
        
        has_optional_prefix, start_idx = structure_info
        tokenized = normalized  # Use normalized tokens for pattern building
        
        # Build pattern from the common structure
        pattern_parts = []
        
        # Handle optional prefix (like opening parenthesis)
        if has_optional_prefix:
            # Get the optional separator from examples that have it
            optional_seps = set()
            for tokens in tokenized:
                if len(tokens) > start_idx and tokens[0][0] == 'sep':
                    sep_value = tokens[0][1]
                    # Check if this is a paired separator like "(" that pairs with ")"
                    if sep_value == '(':
                        # Add as optional opening paren, closing paren will be handled separately
                        optional_seps.add('(')
                    else:
                        optional_seps.add(sep_value)
            
            if optional_seps:
                if len(optional_seps) == 1:
                    sep = list(optional_seps)[0]
                    if sep == '(':
                        # Opening paren - add with optional closing paren
                        pattern_parts.append(r"\(?")
                    else:
                        pattern_parts.append(re.escape(sep) + "?")
                else:
                    escaped = [re.escape(s) for s in sorted(optional_seps)]
                    pattern_parts.append(f"[{''.join(escaped)}]?")
        
        # Find the maximum number of tokens (excluding optional prefix)
        max_tokens = max(len(t) - (1 if has_optional_prefix and t[0][0] == 'sep' else 0) for t in tokenized)
        
        for token_idx in range(max_tokens):
            # Collect tokens at this position from all examples (accounting for optional prefix)
            tokens_at_pos = []
            for tokens in tokenized:
                actual_idx = token_idx + (1 if has_optional_prefix and len(tokens) > start_idx and tokens[0][0] == 'sep' else 0)
                if actual_idx < len(tokens):
                    tokens_at_pos.append(tokens[actual_idx])
            
            if not tokens_at_pos:
                continue
            
            # Analyze token types at this position
            token_types = [t[0] for t in tokens_at_pos]
            
            if all(tt == 'digit' for tt in token_types):
                # All digits - find min and max count
                counts = [t[1] for t in tokens_at_pos]
                min_count = min(counts)
                max_count = max(counts)
                if min_count == max_count:
                    pattern_parts.append(r"\d{" + str(min_count) + "}")
                else:
                    pattern_parts.append(r"\d{" + str(min_count) + "," + str(max_count) + "}")
            
            elif all(tt == 'alpha' for tt in token_types):
                # All letters - find min and max count
                counts = [t[1] for t in tokens_at_pos]
                min_count = min(counts)
                max_count = max(counts)
                
                # Build character class with optional allowed special chars
                char_class = "a-zA-Z"
                if allowed_chars:
                    # Add allowed special characters to the character class
                    allowed_set = self._parse_allowed_chars(allowed_chars)
                    # Escape special regex characters
                    escaped_chars = ''.join(re.escape(c) for c in sorted(allowed_set))
                    char_class = f"a-zA-Z{escaped_chars}"
                
                if min_count == max_count:
                    pattern_parts.append(r"[" + char_class + "]{" + str(min_count) + "}")
                else:
                    pattern_parts.append(r"[" + char_class + "]{" + str(min_count) + "," + str(max_count) + "}")
            
            elif all(tt == 'sep' for tt in token_types):
                # All separators - collect unique separators
                seps = set(t[1] for t in tokens_at_pos)
                
                # Special handling: if we have optional opening paren and this is the first separator after first digit group
                # Check if any separator starts with closing paren
                if has_optional_prefix and token_idx == 1:
                    cleaned_seps = set()
                    has_closing_paren = False
                    for sep in seps:
                        if sep.startswith(')'):
                            has_closing_paren = True
                            # Remove the closing paren, keep the rest
                            rest = sep[1:]
                            if rest:
                                cleaned_seps.add(rest)
                        else:
                            cleaned_seps.add(sep)
                    
                    if has_closing_paren:
                        # Add optional closing paren
                        pattern_parts.append(r"\)?")
                        # Now handle the actual separators
                        if cleaned_seps:
                            if len(cleaned_seps) == 1:
                                pattern_parts.append(re.escape(list(cleaned_seps)[0]))
                            else:
                                escaped = [re.escape(s) for s in sorted(cleaned_seps)]
                                pattern_parts.append(f"[{''.join(escaped)}]")
                        continue
                
                # Normal separator handling
                if len(seps) == 1:
                    # Same separator
                    pattern_parts.append(re.escape(list(seps)[0]))
                else:
                    # Multiple separators - create character class
                    escaped = [re.escape(s) for s in sorted(seps)]
                    pattern_parts.append(f"[{''.join(escaped)}]")
            else:
                # Mixed types at this position - check if some are missing (optional)
                if len(tokens_at_pos) < len(tokenized):
                    # Some examples don't have this token - make it optional
                    # For now, return None as this is complex
                    return None
                else:
                    return None
        
        if pattern_parts:
            return "^" + "".join(pattern_parts) + "$"
        
        return None
    def _generate_char_type_pattern(self, examples: List[str], allowed_chars: Optional[str] = None) -> Optional[str]:
        """
        Generate a pattern based on character types when structured detection fails.
        Useful for cases with optional separators or variable structures.
        
        Args:
            examples: List of example strings
            allowed_chars: Optional comma-separated list of allowed special characters
        """
        if not examples:
            return None
        
        # Analyze what character types are present across all examples
        has_digits = any(any(c.isdigit() for c in ex) for ex in examples)
        has_alpha = any(any(c.isalpha() for c in ex) for ex in examples)
        has_upper = any(any(c.isupper() for c in ex) for ex in examples)
        has_lower = any(any(c.islower() for c in ex) for ex in examples)
        
        # Collect all separator characters
        all_seps = set()
        for ex in examples:
            for c in ex:
                if not c.isalnum():
                    all_seps.add(c)
        
        # Check if examples are primarily digits (phone numbers)
        if has_digits and not has_alpha:
            # Phone number pattern
            digit_counts = [sum(1 for c in ex if c.isdigit()) for ex in examples]
            min_digits = min(digit_counts)
            max_digits = max(digit_counts)
            
            if all_seps:
                # Has separators - make them optional
                # Separate parentheses from other separators
                has_parens = '(' in all_seps or ')' in all_seps
                other_seps = {s for s in all_seps if s not in '()'}
                
                if other_seps:
                    escaped_seps = [re.escape(s) for s in sorted(other_seps)]
                    sep_class = f"[{''.join(escaped_seps)}]?"
                else:
                    sep_class = ""
                
                # Pattern: digits with optional separators between them
                # For phone numbers like 123-45-6789, (555)-33-3333, or 1234567890
                if has_parens:
                    # Pattern with optional parentheses around first group
                    return f"^\\(?\\d{{3}}\\)?{sep_class}\\d{{2,3}}{sep_class}\\d{{4}}$"
                elif min_digits == max_digits:
                    # Try to create a pattern with optional separators
                    # Estimate: typically 3-4 digit groups
                    return f"^\\d{{3}}{sep_class}\\d{{2,3}}{sep_class}\\d{{4}}$"
                else:
                    # Variable length - more flexible
                    return f"^\\d+{sep_class}\\d+{sep_class}\\d+$"
            else:
                # No separators - just digits
                if min_digits == max_digits:
                    return f"^\\d{{{min_digits}}}$"
                else:
                    return f"^\\d{{{min_digits},{max_digits}}}$"
        
        # Check if examples are primarily alpha (emails, domains)
        elif has_alpha:
            # Build character class with optional allowed special chars
            char_class_lower = "a-z"
            char_class_upper = "A-Z"
            char_class_both = "a-zA-Z"
            
            if allowed_chars:
                # Add allowed special characters to the character class
                allowed_set = self._parse_allowed_chars(allowed_chars)
                # Escape special regex characters
                escaped_chars = ''.join(re.escape(c) for c in sorted(allowed_set))
                char_class_lower = f"a-z{escaped_chars}"
                char_class_upper = f"A-Z{escaped_chars}"
                char_class_both = f"a-zA-Z{escaped_chars}"
            
            # Email or domain pattern
            if '@' in all_seps:
                # Email pattern
                # Pattern: word chars + optional dots, @ , word chars + optional dots
                return f"^[{char_class_both}0-9]+(?:\\.[{char_class_both}0-9]+)*@[{char_class_both}0-9]+(?:\\.[{char_class_both}]+)+$"
            elif '.' in all_seps:
                # Domain or dotted name pattern
                if has_upper and has_lower:
                    return f"^[{char_class_both}]+(?:\\.[{char_class_both}]+)+$"
                elif has_upper:
                    return f"^[{char_class_upper}]+(?:\\.[{char_class_upper}]+)+$"
                else:
                    return f"^[{char_class_lower}]+(?:\\.[{char_class_lower}]+)+$"
        
        # Mixed or complex - return None to fall back to other methods
        return None

    
    def _analyze_structure_similarity(self, tokenized: List[List[tuple]]) -> Optional[tuple]:
        """
        Check if tokenized examples have similar structure.
        Expects already-normalized tokens (consecutive separators merged).
        Returns (has_optional_prefix, start_idx) if similar, None otherwise.
        """
        if not tokenized:
            return None
        
        # Get token type sequences (ignoring counts and separator values)
        type_sequences = []
        for tokens in tokenized:
            type_seq = tuple(t[0] for t in tokens)
            type_sequences.append(type_seq)
        
        # Check if all sequences are the same
        unique_sequences = set(type_sequences)
        
        if len(unique_sequences) == 1:
            return (False, 0)  # No optional prefix, start at index 0
        
        # Check if sequences differ only by optional leading separator
        if len(unique_sequences) == 2:
            seqs = list(unique_sequences)
            # Check if one is a prefix of the other (with one extra leading separator)
            if len(seqs[0]) == len(seqs[1]) + 1 and seqs[0][0] == 'sep':
                if seqs[0][1:] == seqs[1]:
                    return (True, 1)  # Has optional prefix, main pattern starts at index 1
            if len(seqs[1]) == len(seqs[0]) + 1 and seqs[1][0] == 'sep':
                if seqs[1][1:] == seqs[0]:
                    return (True, 1)  # Has optional prefix, main pattern starts at index 1
        
        return None

        return pattern
    
    def _generate_flexible_pattern(self, example: str) -> str:
        """Generate a flexible pattern from a single example"""
        pattern_parts = []
        i = 0
        
        while i < len(example):
            char = example[i]
            
            # Look ahead to group consecutive similar characters
            if char.isdigit():
                # Count consecutive digits
                count = 1
                while i + count < len(example) and example[i + count].isdigit():
                    count += 1
                
                if count == 1:
                    pattern_parts.append(r"\d")
                else:
                    pattern_parts.append(r"\d{" + str(count) + "}")
                i += count
                
            elif char.isalpha():
                # Count consecutive letters of same case
                is_upper = char.isupper()
                count = 1
                while i + count < len(example) and example[i + count].isalpha() and example[i + count].isupper() == is_upper:
                    count += 1
                
                if count == 1:
                    pattern_parts.append(r"[A-Z]" if is_upper else r"[a-z]")
                else:
                    pattern_parts.append(r"[A-Z]{" + str(count) + "}" if is_upper else r"[a-z]{" + str(count) + "}")
                i += count
                
            elif char.isspace():
                # Count consecutive spaces
                count = 1
                while i + count < len(example) and example[i + count].isspace():
                    count += 1
                
                if count == 1:
                    pattern_parts.append(r"\s")
                else:
                    pattern_parts.append(r"\s{" + str(count) + "}")
                i += count
                
            else:
                # Special characters - escape them
                pattern_parts.append(re.escape(char))
                i += 1
        
        return "^" + "".join(pattern_parts) + "$"
    
    def _get_char_class(self, chars: List[str]) -> str:
        """Determine character class for a set of characters"""
        unique_chars = set(chars)
        
        if len(unique_chars) == 1:
            # All same character
            return re.escape(chars[0])
        
        # Check if all digits
        if all(c.isdigit() for c in unique_chars):
            return r"\d"
        
        # Check if all letters
        if all(c.isalpha() for c in unique_chars):
            if all(c.isupper() for c in unique_chars):
                return r"[A-Z]"
            elif all(c.islower() for c in unique_chars):
                return r"[a-z]"
            else:
                return r"[a-zA-Z]"
        
        # Check if all alphanumeric
        if all(c.isalnum() for c in unique_chars):
            return r"\w"
        
        # Check if all whitespace
        if all(c.isspace() for c in unique_chars):
            return r"\s"
        
        # Check if all are common separators (for phone numbers, dates, etc.)
        common_separators = {'.', '-', '/', ':', ' ', '(', ')'}
        if unique_chars.issubset(common_separators):
            # Use character class for common separators
            escaped_chars = [re.escape(c) for c in sorted(unique_chars)]
            return f"[{''.join(escaped_chars)}]"
        
        # Mixed - use character set
        escaped_chars = [re.escape(c) for c in unique_chars]
        return f"[{''.join(escaped_chars)}]"
    
    def _find_common_prefix_length(self, strings: List[str]) -> int:
        """Find length of common prefix"""
        if not strings:
            return 0
        
        min_len = min(len(s) for s in strings)
        for i in range(min_len):
            if len(set(s[i] for s in strings)) > 1:
                return i
        return min_len
    
    def _find_common_suffix_length(self, strings: List[str]) -> int:
        """Find length of common suffix"""
        if not strings:
            return 0
        
        min_len = min(len(s) for s in strings)
        for i in range(1, min_len + 1):
            if len(set(s[-i] for s in strings)) > 1:
                return i - 1
        return min_len
    
    def generate_custom_pattern(
        self,
        requirements: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate custom regex pattern based on requirements
        
        Args:
            requirements: Dictionary with pattern requirements
                - min_length: Minimum length
                - max_length: Maximum length
                - must_contain: List of required character types
                - must_start_with: Starting pattern
                - must_end_with: Ending pattern
                - allowed_chars: Allowed character set
                
        Returns:
            Dictionary with generated pattern and metadata
        """
        try:
            pattern_parts = ["^"]
            
            # Starting pattern
            if requirements.get("must_start_with"):
                pattern_parts.append(re.escape(requirements["must_start_with"]))
            
            # Build main pattern based on requirements
            char_class = self._build_char_class(requirements)
            
            min_len = requirements.get("min_length", 1)
            max_len = requirements.get("max_length")
            
            if max_len:
                if min_len == max_len:
                    pattern_parts.append(f"{char_class}{{{min_len}}}")
                else:
                    pattern_parts.append(f"{char_class}{{{min_len},{max_len}}}")
            else:
                if min_len > 1:
                    pattern_parts.append(f"{char_class}{{{min_len},}}")
                else:
                    pattern_parts.append(f"{char_class}+")
            
            # Ending pattern
            if requirements.get("must_end_with"):
                pattern_parts.append(re.escape(requirements["must_end_with"]))
            
            pattern_parts.append("$")
            pattern = "".join(pattern_parts)
            
            return {
                "pattern": pattern,
                "requirements": requirements,
                "confidence": "high",
                "source": "custom_requirements"
            }
            
        except Exception as e:
            logger.error(f"Error generating custom pattern: {str(e)}")
            raise
    
    def _build_char_class(self, requirements: Dict[str, Any]) -> str:
        """Build character class from requirements"""
        if requirements.get("allowed_chars"):
            return f"[{re.escape(requirements['allowed_chars'])}]"
        
        must_contain = requirements.get("must_contain", [])
        
        if not must_contain:
            return r"."
        
        char_classes = []
        if "digits" in must_contain:
            char_classes.append(r"0-9")
        if "lowercase" in must_contain:
            char_classes.append(r"a-z")
        if "uppercase" in must_contain:
            char_classes.append(r"A-Z")
        if "special" in must_contain:
            char_classes.append(r"@$!%*?&")
        
        if char_classes:
            return f"[{''.join(char_classes)}]"
        
        return r"."

# Made with Bob
