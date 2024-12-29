from django.urls import path
from ..views.auth_views import CustomLogoutView

urlpatterns = [
    path('logout/', CustomLogoutView.as_view(), name='logout'),
]