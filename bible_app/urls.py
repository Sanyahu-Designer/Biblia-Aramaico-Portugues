"""Main URL configuration for the Bible app."""
from django.urls import path, include
from .views.cache_monitor import cache_dashboard

app_name = 'bible_app'

urlpatterns = [
    path('', include('bible_app.urls.bible_urls')),
    path('books/', include('bible_app.urls.book_urls')),
    path('chapters/', include('bible_app.urls.chapter_urls')),
    path('verses/', include('bible_app.urls.verse_urls')),
    path('auth/', include('bible_app.urls.auth_urls')),
    path('cache-dashboard/', cache_dashboard, name='cache_dashboard'),
]