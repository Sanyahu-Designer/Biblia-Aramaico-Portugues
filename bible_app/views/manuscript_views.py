from django.shortcuts import render

def manuscripts(request):
    """View for the manuscripts information page."""
    return render(request, 'bible_app/manuscripts.html')
