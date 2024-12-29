from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt, name='dispatch')
class CustomLogoutView(auth_views.LogoutView):
    """
    Custom logout view that handles both admin and regular user logouts
    """
    template_name = 'registration/logged_out.html'
        
    def post(self, request, *args, **kwargs):
        return self.logout(request)

__all__ = ['CustomLogoutView']
