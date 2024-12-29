from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json

@require_POST
def update_theme(request):
    try:
        data = json.loads(request.body)
        theme = data.get('theme')
        
        if theme not in ['light', 'dark']:
            return JsonResponse({'error': 'Invalid theme'}, status=400)
        
        response = JsonResponse({'status': 'success'})
        response.set_cookie('theme', theme, max_age=365*24*60*60)  # 1 year
        return response
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
