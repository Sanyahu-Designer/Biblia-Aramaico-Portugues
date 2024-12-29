"""Utility for monitoring cache and performance metrics."""
from functools import wraps
import time
import logging
from django.core.cache import cache

logger = logging.getLogger(__name__)

class PerformanceMonitor:
    def __init__(self):
        self.cache_hits = 0
        self.cache_misses = 0
        self.response_times = []

    def log_cache_hit(self, key):
        self.cache_hits += 1
        logger.info(f"Cache HIT for key: {key}")

    def log_cache_miss(self, key):
        self.cache_misses += 1
        logger.info(f"Cache MISS for key: {key}")

    def log_response_time(self, duration):
        self.response_times.append(duration)
        logger.info(f"Response time: {duration:.2f}ms")

    def get_stats(self):
        total_requests = self.cache_hits + self.cache_misses
        hit_rate = (self.cache_hits / total_requests * 100) if total_requests > 0 else 0
        avg_response_time = sum(self.response_times) / len(self.response_times) if self.response_times else 0
        
        return {
            'cache_hits': self.cache_hits,
            'cache_misses': self.cache_misses,
            'hit_rate': f"{hit_rate:.1f}%",
            'avg_response_time': f"{avg_response_time:.2f}ms"
        }

performance_monitor = PerformanceMonitor()

def monitor_performance(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        duration = (time.time() - start_time) * 1000  # Convert to milliseconds
        performance_monitor.log_response_time(duration)
        return result
    return wrapper