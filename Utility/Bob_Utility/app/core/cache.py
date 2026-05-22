"""
Caching utilities for the Enterprise Payload Toolkit
"""

from functools import wraps
from typing import Any, Callable, Optional

from cachetools import TTLCache, cached

from app.core.logger import get_logger

logger = get_logger(__name__)

# Default cache configuration
DEFAULT_CACHE_SIZE = 100
DEFAULT_TTL_SECONDS = 3600  # 1 hour

# Global cache instances
_result_cache: TTLCache = TTLCache(maxsize=DEFAULT_CACHE_SIZE, ttl=DEFAULT_TTL_SECONDS)
_parse_cache: TTLCache = TTLCache(maxsize=50, ttl=1800)  # 30 minutes


def get_cache_key(*args: Any, **kwargs: Any) -> str:
    """
    Generate cache key from arguments

    Args:
        *args: Positional arguments
        **kwargs: Keyword arguments

    Returns:
        Cache key string
    """
    key_parts = [str(arg) for arg in args]
    key_parts.extend(f"{k}={v}" for k, v in sorted(kwargs.items()))
    return "|".join(key_parts)


def cache_result(
    ttl: Optional[int] = None, maxsize: Optional[int] = None
) -> Callable:
    """
    Decorator to cache function results

    Args:
        ttl: Time to live in seconds (default: 3600)
        maxsize: Maximum cache size (default: 100)

    Returns:
        Decorated function
    """
    cache = TTLCache(
        maxsize=maxsize or DEFAULT_CACHE_SIZE, ttl=ttl or DEFAULT_TTL_SECONDS
    )

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        @cached(cache=cache)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            logger.debug(f"Cache lookup for {func.__name__}")
            return func(*args, **kwargs)

        # Add cache management methods
        wrapper.cache = cache  # type: ignore
        wrapper.cache_clear = cache.clear  # type: ignore
        wrapper.cache_info = lambda: {  # type: ignore
            "size": len(cache),
            "maxsize": cache.maxsize,
            "ttl": cache.ttl,
        }

        return wrapper

    return decorator


def clear_all_caches() -> None:
    """Clear all global caches"""
    _result_cache.clear()
    _parse_cache.clear()
    logger.info("Cleared all caches")


def get_cache_stats() -> dict[str, Any]:
    """
    Get statistics for all caches

    Returns:
        Dictionary with cache statistics
    """
    return {
        "result_cache": {
            "size": len(_result_cache),
            "maxsize": _result_cache.maxsize,
            "ttl": _result_cache.ttl,
        },
        "parse_cache": {
            "size": len(_parse_cache),
            "maxsize": _parse_cache.maxsize,
            "ttl": _parse_cache.ttl,
        },
    }


class CacheManager:
    """Manager for application-wide caching"""

    def __init__(self, enabled: bool = True) -> None:
        """
        Initialize cache manager

        Args:
            enabled: Whether caching is enabled
        """
        self.enabled = enabled
        self.caches: dict[str, TTLCache] = {
            "result": _result_cache,
            "parse": _parse_cache,
        }
        logger.info(f"CacheManager initialized (enabled={enabled})")

    def get_cache(self, name: str) -> Optional[TTLCache]:
        """
        Get cache by name

        Args:
            name: Cache name

        Returns:
            Cache instance or None
        """
        return self.caches.get(name)

    def create_cache(
        self, name: str, maxsize: int = 100, ttl: int = 3600
    ) -> TTLCache:
        """
        Create a new named cache

        Args:
            name: Cache name
            maxsize: Maximum cache size
            ttl: Time to live in seconds

        Returns:
            New cache instance
        """
        cache = TTLCache(maxsize=maxsize, ttl=ttl)
        self.caches[name] = cache
        logger.info(f"Created cache '{name}' (maxsize={maxsize}, ttl={ttl})")
        return cache

    def clear_cache(self, name: str) -> None:
        """
        Clear specific cache

        Args:
            name: Cache name
        """
        cache = self.caches.get(name)
        if cache:
            cache.clear()
            logger.info(f"Cleared cache '{name}'")

    def clear_all(self) -> None:
        """Clear all caches"""
        for name, cache in self.caches.items():
            cache.clear()
            logger.info(f"Cleared cache '{name}'")

    def get_stats(self) -> dict[str, Any]:
        """
        Get statistics for all caches

        Returns:
            Dictionary with cache statistics
        """
        stats = {}
        for name, cache in self.caches.items():
            stats[name] = {
                "size": len(cache),
                "maxsize": cache.maxsize,
                "ttl": cache.ttl,
            }
        return stats

    def disable(self) -> None:
        """Disable caching"""
        self.enabled = False
        self.clear_all()
        logger.info("Caching disabled")

    def enable(self) -> None:
        """Enable caching"""
        self.enabled = True
        logger.info("Caching enabled")

# Made with Bob
