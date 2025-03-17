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

## Markdown Enrichment

### Metadata Enrichment with OpenAI

The `enrich_markdown.py` script allows you to automatically enhance your markdown files with AI-generated metadata:

#### Prerequisites
- OpenAI API Key
- Python dependencies (install with `pip install -r requirements.txt`)

#### Usage
```bash
# Enrich all markdown files in the 'articles' directory
export OPENAI_API_KEY='your-openai-api-key'
python enrich_markdown.py

# Enrich a specific markdown file
python enrich_markdown.py -f articles/nbnboxes.md

# Enrich markdown files in a different directory
python enrich_markdown.py -d path/to/markdown/files
```

#### What It Does
- Reads markdown files from a specified directory or a specific file
- Generates a concise summary for each article
- Extracts key themes and keywords
- Updates the markdown files' frontmatter with new metadata

## Contributing

Feel free to open issues or submit pull requests to improve the scraper or enrichment script.
