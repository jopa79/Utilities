"""Text processing utilities for manipulating strings.

This module provides functions for text transformation, analysis,
and formatting.
"""

import re

def word_count(text):
    """
    Count the number of words in a text.
    
    Args:
        text (str): The text to analyze
    
    Returns:
        dict: Dictionary with word count statistics
    """
    # Clean the text and split into words
    words = re.findall(r'\b\w+\b', text.lower())
    
    # Count unique words
    unique_words = set(words)
    
    # Count word frequencies
    word_freq = {}
    for word in words:
        word_freq[word] = word_freq.get(word, 0) + 1
    
    # Find most common words
    most_common = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:5]
    
    # Calculate statistics
    stats = {
        'total_words': len(words),
        'unique_words': len(unique_words),
        'word_frequencies': word_freq,
        'most_common': most_common
    }
    
    # Print results
    print(f"Total words: {stats['total_words']}")
    print(f"Unique words: {stats['unique_words']}")
    print("Most common words:")
    for word, count in stats['most_common']:
        print(f"- '{word}': {count} occurrences")
    
    return stats

def format_text(text, case='lower', remove_punctuation=False, remove_numbers=False):
    """
    Format text according to specified options.
    
    Args:
        text (str): The text to format
        case (str): Case formatting ('lower', 'upper', 'title', 'sentence')
        remove_punctuation (bool): Whether to remove punctuation
        remove_numbers (bool): Whether to remove numbers
    
    Returns:
        str: The formatted text
    """
    result = text
    
    # Apply case formatting
    if case == 'lower':
        result = result.lower()
    elif case == 'upper':
        result = result.upper()
    elif case == 'title':
        result = result.title()
    elif case == 'sentence':
        result = '. '.join(s.strip().capitalize() for s in result.split('.'))
    
    # Remove punctuation if requested
    if remove_punctuation:
        result = re.sub(r'[^\w\s]', '', result)
    
    # Remove numbers if requested
    if remove_numbers:
        result = re.sub(r'\d+', '', result)
    
    print("Formatted text:")
    print(result)
    
    return result

def extract_emails(text):
    """
    Extract email addresses from text.
    
    Args:
        text (str): The text to extract emails from
    
    Returns:
        list: List of found email addresses
    """
    # Regular expression for matching email addresses
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    
    # Find all matches
    emails = re.findall(email_pattern, text)
    
    print(f"Found {len(emails)} email addresses:")
    for email in emails:
        print(f"- {email}")
    
    return emails