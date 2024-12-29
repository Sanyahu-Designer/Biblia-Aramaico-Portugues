"""Service for handling user preferences."""
from django.db.models import QuerySet
from django.contrib.auth.models import User
from ..models import UserPreference

class PreferencesService:
    @staticmethod
    def get_user_preferences(user_id: int) -> dict:
        """Get user preferences."""
        prefs, _ = UserPreference.objects.get_or_create(user_id=user_id)
        return {
            'theme': prefs.theme,
            'font_size': prefs.font_size,
            'show_transliteration': prefs.show_transliteration,
            'show_pronunciation': prefs.show_pronunciation,
            'show_word_analysis': prefs.show_word_analysis
        }
        
    @staticmethod
    def update_preferences(user_id: int, **preferences) -> UserPreference:
        """Update user preferences."""
        prefs, _ = UserPreference.objects.get_or_create(user_id=user_id)
        for key, value in preferences.items():
            if hasattr(prefs, key):
                setattr(prefs, key, value)
        prefs.save()
        return prefs
        
    @staticmethod
    def reset_preferences(user_id: int) -> UserPreference:
        """Reset user preferences to defaults."""
        prefs, _ = UserPreference.objects.get_or_create(user_id=user_id)
        prefs.theme = 'light'
        prefs.font_size = 16
        prefs.show_transliteration = True
        prefs.show_pronunciation = True
        prefs.show_word_analysis = True
        prefs.save()
        return prefs