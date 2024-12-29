from django.urls import path
from bible_app.views.bible_views import home, get_chapters
from bible_app.views.theme_views import update_theme
from bible_app.views.search_views import search_content
from bible_app.views.manuscript_views import manuscripts

urlpatterns = [
    path('', home, name='home'),
    path('manuscripts/', manuscripts, name='manuscripts'),
    path('get-chapters/', get_chapters, name='get_chapters'),
    path('search/', search_content, name='search'),
    path('update-theme/', update_theme, name='update_theme'),
]