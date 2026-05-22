"""
Common utility functions for the Enterprise Payload Toolkit
"""

import hashlib
import re
from datetime import datetime
from typing import Any


def generate_id(prefix: str = "") -> str:
    """
    Generate a unique ID with optional prefix

    Args:
        prefix: Optional prefix for the ID

    Returns:
        Unique ID string
    """
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
    if prefix:
        return f"{prefix}_{timestamp}"
    return timestamp


def calculate_hash(content: str, algorithm: str = "sha256") -> str:
    """
    Calculate hash of content

    Args:
        content: Content to hash
        algorithm: Hash algorithm (md5, sha1, sha256, sha512)

    Returns:
        Hex digest of the hash
    """
    hash_func = getattr(hashlib, algorithm)
    return hash_func(content.encode()).hexdigest()


def truncate_string(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    Truncate string to maximum length

    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add if truncated

    Returns:
        Truncated string
    """
    if len(text) <= max_length:
        return text
    return text[: max_length - len(suffix)] + suffix


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename by removing invalid characters

    Args:
        filename: Original filename

    Returns:
        Sanitized filename
    """
    # Remove invalid characters
    sanitized = re.sub(r'[<>:"/\\|?*]', "_", filename)
    # Remove leading/trailing spaces and dots
    sanitized = sanitized.strip(". ")
    return sanitized or "unnamed"


def format_bytes(bytes_size: int) -> str:
    """
    Format bytes to human-readable string

    Args:
        bytes_size: Size in bytes

    Returns:
        Formatted string (e.g., "1.5 MB")
    """
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if bytes_size < 1024.0:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.2f} PB"


def deep_get(dictionary: dict, keys: str, default: Any = None) -> Any:
    """
    Get nested dictionary value using dot notation

    Args:
        dictionary: Dictionary to search
        keys: Dot-separated keys (e.g., "user.profile.name")
        default: Default value if key not found

    Returns:
        Value at the specified path or default
    """
    keys_list = keys.split(".")
    value = dictionary

    for key in keys_list:
        if isinstance(value, dict):
            value = value.get(key)
            if value is None:
                return default
        else:
            return default

    return value


def deep_set(dictionary: dict, keys: str, value: Any) -> None:
    """
    Set nested dictionary value using dot notation

    Args:
        dictionary: Dictionary to modify
        keys: Dot-separated keys (e.g., "user.profile.name")
        value: Value to set
    """
    keys_list = keys.split(".")
    current = dictionary

    for key in keys_list[:-1]:
        if key not in current or not isinstance(current[key], dict):
            current[key] = {}
        current = current[key]

    current[keys_list[-1]] = value


def flatten_dict(
    dictionary: dict, parent_key: str = "", separator: str = "."
) -> dict:
    """
    Flatten nested dictionary

    Args:
        dictionary: Dictionary to flatten
        parent_key: Parent key prefix
        separator: Separator for keys

    Returns:
        Flattened dictionary
    """
    items: list[tuple[str, Any]] = []

    for key, value in dictionary.items():
        new_key = f"{parent_key}{separator}{key}" if parent_key else key

        if isinstance(value, dict):
            items.extend(flatten_dict(value, new_key, separator).items())
        else:
            items.append((new_key, value))

    return dict(items)


def unflatten_dict(dictionary: dict, separator: str = ".") -> dict:
    """
    Unflatten dictionary with dot-separated keys

    Args:
        dictionary: Flattened dictionary
        separator: Key separator

    Returns:
        Nested dictionary
    """
    result: dict = {}

    for key, value in dictionary.items():
        deep_set(result, key.replace(separator, "."), value)

    return result


def is_valid_regex(pattern: str) -> bool:
    """
    Check if a string is a valid regex pattern

    Args:
        pattern: Regex pattern to validate

    Returns:
        True if valid, False otherwise
    """
    try:
        re.compile(pattern)
        return True
    except re.error:
        return False


def extract_numbers(text: str) -> list[float]:
    """
    Extract all numbers from text

    Args:
        text: Text to extract numbers from

    Returns:
        List of numbers found
    """
    pattern = r"-?\d+\.?\d*"
    matches = re.findall(pattern, text)
    return [float(match) for match in matches]


def count_lines(text: str) -> int:
    """
    Count number of lines in text

    Args:
        text: Text to count lines in

    Returns:
        Number of lines
    """
    return len(text.splitlines())


def remove_empty_lines(text: str) -> str:
    """
    Remove empty lines from text

    Args:
        text: Text to process

    Returns:
        Text without empty lines
    """
    lines = [line for line in text.splitlines() if line.strip()]
    return "\n".join(lines)


def indent_text(text: str, spaces: int = 2) -> str:
    """
    Indent all lines in text

    Args:
        text: Text to indent
        spaces: Number of spaces to indent

    Returns:
        Indented text
    """
    indent = " " * spaces
    lines = text.splitlines()
    return "\n".join(f"{indent}{line}" for line in lines)


def normalize_line_endings(text: str, ending: str = "\n") -> str:
    """
    Normalize line endings in text

    Args:
        text: Text to normalize
        ending: Desired line ending (\n or \r\n)

    Returns:
        Text with normalized line endings
    """
    # Replace all line endings with \n first
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    # Then replace with desired ending if different
    if ending != "\n":
        text = text.replace("\n", ending)
    return text

# Made with Bob
