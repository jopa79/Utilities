"""File operation utilities for working with files and directories.

This module provides common file operations like listing files,
counting lines in files, and searching for text in files.
"""

import os
import glob

def list_files(directory=".", pattern="*.*"):
    """
    List all files in a directory that match the given pattern.
    
    Args:
        directory (str): Directory path to search in. Defaults to current directory.
        pattern (str): File pattern to match. Defaults to all files.
    
    Returns:
        list: List of file paths that match the pattern
    """
    search_path = os.path.join(directory, pattern)
    files = glob.glob(search_path)
    
    print(f"Found {len(files)} files matching '{pattern}' in '{directory}':")
    for file in files:
        print(f"- {file}")
    
    return files

def count_lines(file_path):
    """
    Count the number of lines in a text file.
    
    Args:
        file_path (str): Path to the file
    
    Returns:
        int: Number of lines in the file
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            line_count = sum(1 for _ in file)
        
        print(f"File '{file_path}' contains {line_count} lines.")
        return line_count
    
    except Exception as e:
        print(f"Error counting lines in '{file_path}': {str(e)}")
        return -1

def search_text(file_path, search_term, case_sensitive=False):
    """
    Search for text in a file and display matching lines.
    
    Args:
        file_path (str): Path to the file
        search_term (str): Text to search for
        case_sensitive (bool): Whether the search should be case-sensitive
    
    Returns:
        list: List of tuples containing (line_number, line_text) for matches
    """
    try:
        matches = []
        
        with open(file_path, 'r', encoding='utf-8') as file:
            for i, line in enumerate(file, 1):
                if (search_term in line) if case_sensitive else (search_term.lower() in line.lower()):
                    matches.append((i, line.strip()))
        
        print(f"Found {len(matches)} matches for '{search_term}' in '{file_path}':")
        for line_num, line_text in matches:
            print(f"Line {line_num}: {line_text}")
        
        return matches
    
    except Exception as e:
        print(f"Error searching text in '{file_path}': {str(e)}")
        return []