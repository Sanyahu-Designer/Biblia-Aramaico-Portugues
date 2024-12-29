"""Utility functions for caching."""
from django.core.cache import cache
from django.conf import settings
from functools import wraps
import hashlib
import json
import logging
from ..utils.cache_stats import cache_stats

logger = logging.getLogger(__name__)

# Cache timeouts in seconds
CACHE_TIMEOUTS = {
    'static': 86400,    # 24 hours for static data like books
    'dynamic': 3600,    # 1 hour for dynamic content like verses
    'search': 1800,     # 30 minutes for search results
    'navigation': 600,  # 10 minutes for navigation data
}

def generate_cache_key(prefix: str, *args, **kwargs) -> str:
    """Generate a unique cache key based on arguments.
    
    Args:
        prefix: String prefix for the cache key
        *args: Positional arguments to include in key generation
        **kwargs: Keyword arguments to include in key generation
        
    Returns:
        str: Generated cache key
    """
    try:
        # Convert args and kwargs to strings
        key_parts = [str(arg) for arg in args]
        key_parts.extend(f"{k}:{v}" for k, v in sorted(kwargs.items()))
        
        # Join parts and hash
        key_string = ":".join(key_parts)
        hashed = hashlib.md5(key_string.encode()).hexdigest()
        
        return f"{prefix}:{hashed}"
    except Exception as e:
        logger.error(f"Error generating cache key: {str(e)}")
        return f"{prefix}:fallback"

def cache_response(timeout=None, prefix='view'):
    """Cache decorator for views.
    
    Args:
        timeout: Cache timeout in seconds (defaults to dynamic content timeout)
        prefix: String prefix for the cache key
        
    Returns:
        function: Decorated view function
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if request.method != 'GET':
                return view_func(request, *args, **kwargs)

            # Use provided timeout or default dynamic timeout
            cache_timeout = timeout or CACHE_TIMEOUTS['dynamic']
            
            # Generate cache key including query parameters
            cache_key = generate_cache_key(
                prefix,
                request.path,
                request.GET.dict(),
                *args,
                **kwargs
            )
            
            # Try to get from cache
            response = cache.get(cache_key)
            
            if response is None:
                response = view_func(request, *args, **kwargs)
                cache.set(cache_key, response, cache_timeout)
                logger.debug(f"Cache miss for key: {cache_key}")
                cache_stats.record_hit(cache_key, 'miss')
            else:
                logger.debug(f"Cache hit for key: {cache_key}")
                cache_stats.record_hit(cache_key, 'hit')
            
            return response
        return wrapper
    return decorator

def cache_queryset(timeout=None, prefix='queryset'):
    """Cache decorator for querysets.
    
    Args:
        timeout: Cache timeout in seconds (defaults to dynamic content timeout)
        prefix: String prefix for the cache key
        
    Returns:
        function: Decorated function
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Use provided timeout or default dynamic timeout
            cache_timeout = timeout or CACHE_TIMEOUTS['dynamic']
            
            # Generate cache key
            cache_key = generate_cache_key(prefix, func.__name__, *args, **kwargs)
            
            # Try to get from cache
            result = cache.get(cache_key)
            
            if result is None:
                result = func(*args, **kwargs)
                cache.set(cache_key, result, cache_timeout)
                logger.debug(f"Cache miss for queryset: {cache_key}")
                cache_stats.record_hit(cache_key, 'miss')
            else:
                logger.debug(f"Cache hit for queryset: {cache_key}")
                cache_stats.record_hit(cache_key, 'hit')
            
            return result
        return wrapper
    return decorator

def invalidate_cache_prefix(prefix: str) -> None:
    """Invalidate all cache keys with the given prefix.
    
    Args:
        prefix: String prefix to invalidate
    """
    try:
        if hasattr(cache, 'delete_pattern'):
            # For Redis and similar backends that support pattern deletion
            cache.delete_pattern(f"{prefix}:*")
            logger.info(f"Invalidated cache pattern: {prefix}:*")
        else:
            # Fallback for backends that don't support pattern deletion
            logger.warning("Cache backend doesn't support pattern deletion")
    except Exception as e:
        logger.error(f"Error invalidating cache: {str(e)}")

def cache_navigation(timeout=None):
    """Special decorator for caching navigation-related data.
    
    Args:
        timeout: Cache timeout in seconds (defaults to navigation timeout)
        
    Returns:
        function: Decorated function
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            cache_timeout = timeout or CACHE_TIMEOUTS['navigation']
            cache_key = generate_cache_key('navigation', func.__name__, *args, **kwargs)
            
            result = cache.get(cache_key)
            
            if result is None:
                result = func(*args, **kwargs)
                cache.set(cache_key, result, cache_timeout)
                logger.debug(f"Cache miss for navigation: {cache_key}")
                cache_stats.record_hit(cache_key, 'miss')
            else:
                logger.debug(f"Cache hit for navigation: {cache_key}")
                cache_stats.record_hit(cache_key, 'hit')
            
            return result
        return wrapper
    return decorator

def cache_static_data(timeout=None):
    """Decorator for caching static data like books and chapters.
    
    Args:
        timeout: Cache timeout in seconds (defaults to static content timeout)
        
    Returns:
        function: Decorated function
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            cache_timeout = timeout or CACHE_TIMEOUTS['static']
            cache_key = generate_cache_key('static', func.__name__, *args, **kwargs)
            
            result = cache.get(cache_key)
            
            if result is None:
                result = func(*args, **kwargs)
                cache.set(cache_key, result, cache_timeout)
                logger.debug(f"Cache miss for static data: {cache_key}")
                cache_stats.record_hit(cache_key, 'miss')
            else:
                logger.debug(f"Cache hit for static data: {cache_key}")
                cache_stats.record_hit(cache_key, 'hit')
            
            return result
        return wrapper
    return decorator

def clear_all_caches() -> None:
    """Clear all caches in the application."""
    try:
        cache.clear()
        logger.info("Cleared all caches successfully")
    except Exception as e:
        logger.error(f"Error clearing caches: {str(e)}")