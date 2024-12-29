"""Utility for tracking and reporting cache statistics."""
from django.core.cache import cache
from datetime import datetime, timedelta
import json

class CacheStats:
    def __init__(self):
        self.stats_key = 'cache_statistics'
        self._load_stats()

    def _load_stats(self):
        stats = cache.get(self.stats_key)
        if not stats:
            self.stats = {
                'daily_hits': {},
                'content_types': {
                    'hit': 0,
                    'miss': 0
                }
            }
        else:
            self.stats = json.loads(stats)

    def _save_stats(self):
        cache.set(self.stats_key, json.dumps(self.stats), None)

    def record_hit(self, key: str, hit_type: str):
        """Record a cache hit or miss.
        
        Args:
            key: Cache key that was accessed
            hit_type: Type of access ('hit' or 'miss')
        """
        today = datetime.now().strftime('%Y-%m-%d')
        
        # Update daily hits
        if today not in self.stats['daily_hits']:
            self.stats['daily_hits'][today] = {
                'hit': 0,
                'miss': 0
            }
        self.stats['daily_hits'][today][hit_type] += 1

        # Update content type stats
        self.stats['content_types'][hit_type] += 1

        self._save_stats()

    def get_daily_stats(self, days=7):
        """Get daily statistics for the specified number of days.
        
        Args:
            days: Number of days to return stats for
            
        Returns:
            list: List of daily statistics
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days-1)
        
        daily_stats = []
        current_date = start_date
        
        while current_date <= end_date:
            date_str = current_date.strftime('%Y-%m-%d')
            stats = self.stats['daily_hits'].get(date_str, {'hit': 0, 'miss': 0})
            daily_stats.append({
                'date': date_str,
                'hits': stats['hit'],
                'misses': stats['miss']
            })
            current_date += timedelta(days=1)
        
        return daily_stats

    def get_content_type_stats(self):
        """Get statistics by content type.
        
        Returns:
            dict: Dictionary of content type statistics
        """
        return self.stats['content_types']

    def clear_old_stats(self, days=30):
        """Clear statistics older than the specified number of days.
        
        Args:
            days: Number of days of stats to keep
        """
        cutoff_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        
        # Remove old daily stats
        self.stats['daily_hits'] = {
            date: hits 
            for date, hits in self.stats['daily_hits'].items() 
            if date >= cutoff_date
        }
        
        self._save_stats()

cache_stats = CacheStats()