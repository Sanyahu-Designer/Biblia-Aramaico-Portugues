from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from bible_app.views.auth_views import CustomLogoutView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import views

admin.site.site_header = 'Evangelhos Aramaico Siriaco'
admin.site.site_title = 'Evangelhos Aramaico Siriaco'
admin.site.index_title = 'Administração'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('bible_app.urls', namespace='bible_app')),
    path('dictionary/', include('dictionary_app.urls', namespace='dictionary')),
    path('banners/', include('banners.urls', namespace='banners')),
    path('update-theme/', views.update_theme, name='update_theme'),
]

# Adicionar URLs para arquivos estáticos e de mídia em desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += staticfiles_urlpatterns()
else:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
