from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Book, Chapter, Verse
from dictionary_app.models import AramaicWord

class StaticViewSitemap(Sitemap):
    priority = 1.0
    changefreq = 'weekly'

    def items(self):
        return ['bible_app:home']

    def location(self, item):
        return reverse(item)

class BookSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8

    def items(self):
        return Book.objects.all()

    def location(self, obj):
        return reverse('bible_app:book_chapters', args=[obj.id])

class ChapterSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.7

    def items(self):
        return Chapter.objects.all()

    def location(self, obj):
        return reverse('bible_app:book_chapters', args=[obj.book.id])

class VerseSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.6

    def items(self):
        return Verse.objects.all()

    def location(self, obj):
        return f'/verses/{obj.id}/'

class WordSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return AramaicWord.objects.all()

    def location(self, obj):
        return f'/dictionary/word/{obj.id}/'
