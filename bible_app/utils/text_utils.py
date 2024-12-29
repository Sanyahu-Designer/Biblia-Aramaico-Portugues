"""Utility functions for text processing and formatting."""

def format_verse_reference(book_name: str, chapter_number: int, verse_number: int) -> str:
    """Format a Bible verse reference in a standard format.
    
    Args:
        book_name (str): Name of the book
        chapter_number (int): Chapter number
        verse_number (int): Verse number
        
    Returns:
        str: Formatted verse reference (e.g., "Genesis 1:1")
    """
    return f"{book_name} {chapter_number}:{verse_number}"

def format_chapter_reference(book_name: str, chapter_number: int) -> str:
    """Format a Bible chapter reference.
    
    Args:
        book_name (str): Name of the book
        chapter_number (int): Chapter number
        
    Returns:
        str: Formatted chapter reference (e.g., "Genesis 1")
    """
    return f"{book_name} {chapter_number}"