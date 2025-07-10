# Simple Markdown Blog

This project is a minimal blog system written in Python using Flask.
It supports writing posts in Markdown and renders them with a clean
Bulma-based user interface.

## Features

- Create, edit, and view blog posts
- Posts written in Markdown
- SQLite database
- Responsive, modern design using Bulma CSS

## Setup

1. Create a virtual environment (optional but recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python app.py
   ```
   The blog will be available at `http://localhost:5000`.

## Notes

This is a simple demo application. It does not include authentication
or advanced features, but serves as a foundation for a lightweight blog
system that renders Markdown content with a pleasant aesthetic.
