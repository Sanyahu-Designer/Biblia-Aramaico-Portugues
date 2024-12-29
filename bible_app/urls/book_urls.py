"""URLs for Book-related views."""
from django.urls import path
from ..views.book_views import book_chapters, add_chapter

urlpatterns = [
    path('<int:book_id>/chapters/', book_chapters, name='book_chapters'),
    path('<int:book_id>/chapters/add/', add_chapter, name='add_chapter'),
]