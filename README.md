# Superloop Support Article Scraper

## Overview

This Python script scrapes support articles from the Superloop support website using the sitemap and direct API calls.

## Prerequisites

- Python 3.7+
- `uv` package manager

## Setup

1. Install dependencies:
```bash
uv add requests xmltodict html2text
```

## Usage

### Basic Scraping
Scrape all articles from the sitemap:
```bash
python scrape_articles.py
```

### Limit Number of Articles
Scrape a specific number of articles (e.g., first 5):
```bash
python scrape_articles.py 5
```

## Output

- Articles are saved as Markdown files in the `articles/` directory
- Each file is named after the article's page name
- Markdown files include:
  - YAML frontmatter with:
    - Title
    - Article Number
    - Source URL
  - Article content converted to Markdown

## Features

- Direct API-based scraping
- Converts HTML to Markdown
- Supports partial scraping
- Extracts full article details

## Limitations

- Depends on current API structure
- May require updates if website changes

## Contributing

Feel free to open issues or submit pull requests to improve the scraper.
