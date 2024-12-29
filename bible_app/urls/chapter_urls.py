"""URLs for Chapter-related views."""
from django.urls import path
from ..views.chapter_views import chapter_verses, add_verse

urlpatterns = [
    path('<int:chapter_id>/verses/', chapter_verses, name='chapter_verses'),
    path('<int:chapter_id>/verses/add/', add_verse, name='add_verse'),
]