"""Unit conversion utilities.

This module provides functions for converting between different units
of measurement including length, weight, temperature, and more.
"""

def celsius_to_fahrenheit(celsius: float) -> float:
    """
    Convert Celsius to Fahrenheit.
    
    Args:
        celsius (float): Temperature in Celsius
    
    Returns:
        float: Temperature in Fahrenheit
    """
    fahrenheit = (celsius * 9/5) + 32
    print(f"{celsius}°C = {fahrenheit}°F")
    return fahrenheit

def fahrenheit_to_celsius(fahrenheit: float) -> float:
    """
    Convert Fahrenheit to Celsius.
    
    Args:
        fahrenheit (float): Temperature in Fahrenheit
    
    Returns:
        float: Temperature in Celsius
    """
    celsius = (fahrenheit - 32) * 5/9
    print(f"{fahrenheit}°F = {celsius}°C")
    return celsius

def kilometers_to_miles(kilometers: float) -> float:
    """
    Convert kilometers to miles.
    
    Args:
        kilometers (float): Distance in kilometers
    
    Returns:
        float: Distance in miles
    """
    miles = kilometers * 0.621371
    print(f"{kilometers} km = {miles} miles")
    return miles

def miles_to_kilometers(miles: float) -> float:
    """
    Convert miles to kilometers.
    
    Args:
        miles (float): Distance in miles
    
    Returns:
        float: Distance in kilometers
    """
    kilometers = miles * 1.60934
    print(f"{miles} miles = {kilometers} km")
    return kilometers

def kilograms_to_pounds(kilograms: float) -> float:
    """
    Convert kilograms to pounds.
    
    Args:
        kilograms (float): Weight in kilograms
    
    Returns:
        float: Weight in pounds
    """
    pounds = kilograms * 2.20462
    print(f"{kilograms} kg = {pounds} lbs")
    return pounds

def pounds_to_kilograms(pounds: float) -> float:
    """
    Convert pounds to kilograms.
    
    Args:
        pounds (float): Weight in pounds
    
    Returns:
        float: Weight in kilograms
    """
    kilograms = pounds * 0.453592
    print(f"{pounds} lbs = {kilograms} kg")
    return kilograms