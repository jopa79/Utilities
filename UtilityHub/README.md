# Utility Hub Application

A GUI application that automatically discovers and loads Python utility scripts in the current directory. It serves as a central hub for running utility functions, displaying their outputs, and managing their parameters.

## Features

- Automatically discovers and loads all Python files that start with `util` in the same directory
- Displays a list of available utility modules
- Shows module documentation and available functions
- Dynamically creates parameter input fields based on function signatures
- Captures and displays function output in a console window
- Supports various parameter types including strings, numbers, and booleans

## How to Use

1. Place your utility scripts (Python files that start with `util`) in the same directory as the hub application
2. Run the hub application: `python utility_hub.py`
3. Select a utility module from the list on the left
4. Choose a function from the dropdown menu
5. Fill in the required parameters
6. Click "Execute" to run the selected function

## Creating Compatible Utility Scripts

For best results, follow these guidelines when creating utility scripts:

1. Name your Python files starting with `util`, e.g., `util_math.py`, `util_files.py`, etc.
2. Include a module-level docstring that describes the utility's purpose
3. Create functions with descriptive names and docstrings
4. Use type annotations for parameters to help the hub create appropriate input widgets
5. Print informative output messages to provide feedback to the user

Example:

```python
"""Math utility functions.

This module provides basic mathematical operations and conversions.
"""

def calculate_area(length: float, width: float) -> float:
    """
    Calculate the area of a rectangle.
    
    Args:
        length (float): The length of the rectangle
        width (float): The width of the rectangle
        
    Returns:
        float: The area of the rectangle
    """
    area = length * width
    print(f"The area of a {length} x {width} rectangle is {area}.")
    return area
```

## Adding More Utility Scripts

Simply create new Python files that start with `util` and place them in the same directory as the hub application. The next time you run the application, they will be automatically discovered and loaded.

## Requirements

- Python 3.6 or higher
- tkinter (usually included with Python installations)