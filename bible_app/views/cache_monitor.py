"""View for monitoring cache performance."""
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from ..utils.cache_stats import cache_stats

@staff_member_required
def cache_dashboard(request):
    """Dashboard view for monitoring cache performance."""
    content_stats = cache_stats.get_content_type_stats()
    daily_stats = cache_stats.get_daily_stats()
    
    total_requests = content_stats['hit'] + content_stats['miss']
    hit_rate = round((content_stats['hit'] / total_requests * 100) if total_requests > 0 else 0, 1)
    
    context = {
        'title': 'Dashboard de Cache',
        'daily_stats': daily_stats,
        'content_stats': content_stats,
        'total_requests': total_requests,
        'hit_rate': hit_rate
    }
    return render(request, 'admin/cache_dashboard.html', context)