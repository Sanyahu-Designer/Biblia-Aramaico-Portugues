from django.urls import path
from . import views

app_name = 'banners'

urlpatterns = [
    path('api/next-banner/', views.get_next_banner, name='next_banner'),
    path('api/register-click/<int:banner_id>/', views.register_click, name='register_click'),
    path('api/register-view/<int:banner_id>/', views.register_view, name='register_view'),
    path('media/banners/<str:filename>', views.serve_banner_image, name='serve_banner'),
]
