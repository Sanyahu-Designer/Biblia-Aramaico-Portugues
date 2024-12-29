"""URLs for Verse-related views."""
from django.urls import path
from ..views.verse_views import verse_detail, edit_verse

urlpatterns = [
    path('<int:verse_id>/', verse_detail, name='verse_detail'),
    path('<int:verse_id>/edit/', edit_verse, name='edit_verse'),
]