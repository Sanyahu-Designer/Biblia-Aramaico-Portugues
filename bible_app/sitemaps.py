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
        return reverse('bible_app:book_detail', args=[obj.slug])

    def lastmod(self, obj):
        return obj.updated_at

class ChapterSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.7

    def items(self):
        return Chapter.objects.all()

    def location(self, obj):
        return reverse('bible_app:chapter_detail', args=[obj.book.slug, obj.number])

    def lastmod(self, obj):
        return obj.updated_at

class VerseSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.6

    def items(self):
        return Verse.objects.all()

    def location(self, obj):
        return reverse('bible_app:verse_detail', args=[obj.chapter.book.slug, obj.chapter.number, obj.number])

    def lastmod(self, obj):
        return obj.updated_at

class WordSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return AramaicWord.objects.all()

    def location(self, obj):
        return reverse('dictionary_app:word_detail', args=[obj.id])

    def lastmod(self, obj):
        return obj.updated_at
