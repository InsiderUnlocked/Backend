# @Author: Mohammed-Al Rasheed
# Purpose: This file contains a function which cleans texts. By this we mean remove unneccasery characters and remove new lines, tabs, and whitespaces.

# Import Libraries
import re

# Cleans the text by removing all unneccasery characters
def cleanText(text):
    # removes some symbols
    text = re.sub('\[.*?\]', ' ', text)
    # removes some symbols
    text = re.sub('<.*?>+', ' ', text)
    # removes new lines \n
    text = re.sub('\n', ' ', text)
    # Removes tabs
    text = re.sub('\t', ' ', text)
    # Remove duplicate whitespaces characters 
    text = re.sub('\s+', ' ', text).strip()
    
    # Retur the text as a string
    return str(text)

