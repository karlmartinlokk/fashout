# Fashout

A social network for sharing outfits. Users post photos of their fits, list the pieces they're wearing, and follow, like and comment on each other's posts.

Built solo (Jan 2024 – Feb 2025) while studying at Tallinna Reaalkool, using the Django skills I learned in the school's official programming track. The main goal was to build something bigger on my own, with a side effect of learning HTML and CSS (but ended up picking up a bit of JavaScript too)

**Status:** unfinished, no longer in active development. The core social features work; the OOTD, style guide and about pages are still placeholders.

## Features

- User registration, login and logout
- Profiles with profile pictures (auto-resized with Pillow)
- Following / unfollowing other users
- Uploading outfit posts with an image, caption and list of pieces
- Feed for browsing posts
- Viewing, editing and deleting your own posts
- Likes and comments
- User search

## Tech stack

- Python, Django 5
- vanilla HTML, CSS, JavaScript
- SQLite

## Running locally

```bash
pip install -r requirements.txt
cp .env.example .env   # then set SECRET_KEY to a random string
python manage.py migrate
python manage.py runserver
```
