from django.urls import path, include

app_name = 'bible_app'

urlpatterns = [
    path('', include('bible_app.urls.bible_urls')),
    path('auth/', include('bible_app.urls.auth_urls')),
    ]
