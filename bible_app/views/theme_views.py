from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from ..services.preferences_service import PreferencesService
import json

@csrf_exempt
def update_theme(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            theme = data.get('theme')
            if theme in ['light', 'dark']:
                response = JsonResponse({'status': 'success', 'message': 'Theme updated successfully'})
                response.set_cookie('theme', theme, max_age=31536000)  # Armazena o tema por 1 ano
                return response
            else:
                return JsonResponse({'status': 'error', 'message': 'Invalid theme'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)
