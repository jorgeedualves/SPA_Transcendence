#!/bin/bash

# Find and remove all __pycache__ directories
find . -type d -name "__pycache__" -exec rm -r {} +

# Run the Django development server
python3 manage.py runserver
