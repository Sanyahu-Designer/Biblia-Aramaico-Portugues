"""Main URL configuration for the Bible app."""
from django.urls import path, include
from .views.cache_monitor import cache_dashboard
from .views.bible_views import home, get_chapters, search

app_name = 'bible_app'

urlpatterns = [
    path('', home, name='home'),
    path('books/', include('bible_app.urls.book_urls')),
    path('verses/', include('bible_app.urls.verse_urls')),
    path('auth/', include('bible_app.urls.auth_urls')),
    path('chapters/', get_chapters, name='get_chapters'),
    path('search/', search, name='search'),
    path('cache-dashboard/', cache_dashboard, name='cache_dashboard'),
]