from django.urls import path
from . import views

app_name = 'dictionary'

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search_words, name='search_words'),
    path('word/<int:word_id>/details/', views.word_details, name='word_details'),
    path('word/add/', views.edit_word, name='add_word'),
    path('word/<int:word_id>/edit/', views.edit_word, name='edit_word'),
    path('detect-occurrences/', views.detect_occurrences, name='detect_occurrences'),
    path('word/toggle-favorite/', views.toggle_favorite, name='toggle_favorite'),
]
