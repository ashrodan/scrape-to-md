import os
import json
import xmltodict
import requests
import html2text

def parse_sitemap(sitemap_path, max_pages=None):
    """Parse the XML sitemap and extract URLs and page names."""
    with open(sitemap_path, 'r') as f:
        sitemap_content = f.read()
    
    sitemap_dict = xmltodict.parse(sitemap_content)
    urls = [url['loc'] for url in sitemap_dict['urlset']['url']]
    
    # Extract page names from URLs
    page_names = [url.split('/')[-1] for url in urls]
    
    return page_names[:max_pages] if max_pages is not None else page_names

def fetch_article_info(page_name):
    """Fetch article information from Superloop API."""
    base_url = "https://support.superloop.com/webruntime/api/apex/execute"
    
    # Construct the API parameters
    params = {
        "cacheable": "true",
        "classname": "@udd/01p2t000002XhW5/NS",
        "isContinuation": "false",
        "method": "getArticleInfoLightning",
        "namespace": "articleBody",
        "params": json.dumps({
            "articleAPIName": "Knowledge__kav",
            "articleBodyAPIName": "Knowledge_Articles_Exetel_Description__c",
            "articleBodyAPIName2": "",
            "articleNumber": "",
            "initial": True,
            "queryBy": "urlName",
            "recordId": "",  # This seems to be dynamic, but not critical
            "urlName": page_name
        }),
        "language": "en-US",
        "asGuest": "true",
        "htmlEncode": "false"
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        
        # Parse the JSON response
        data = response.json()
        
        # The returnValue is a JSON string, so we need to parse it again
        article_data = json.loads(data['returnValue'])
        
        # Convert HTML to Markdown
        h = html2text.HTML2Text()
        h.ignore_links = False
        h.ignore_images = False
        markdown_body = h.handle(article_data.get('body', ''))
        
        return {
            'article_number': article_data.get('articleNumber', ''),
            'title': article_data.get('title', ''),
            'body': markdown_body,
            'url': f"https://support.superloop.com/support-hub-article/{page_name}"
        }
    
    except (requests.RequestException, json.JSONDecodeError, KeyError) as e:
        print(f"Error fetching article for {page_name}: {e}")
        return None

def main(sitemap_path, max_pages=None, output_dir='articles'):
    """Main function to scrape articles from sitemap."""
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Parse sitemap and get page names
    page_names = parse_sitemap(sitemap_path, max_pages)
    
    # Scrape and save each article
    for i, page_name in enumerate(page_names, 1):
        print(f"Scraping article {i}/{len(page_names)}: {page_name}")
        article_info = fetch_article_info(page_name)
        
        if article_info:
            # Create markdown content with frontmatter
            markdown_content = f"""---
title: {article_info['title']}
article_number: {article_info['article_number']}
source_url: {article_info['url']}
---

{article_info['body']}
"""
            
            # Create filename from page name
            filename = page_name + '.md'
            filepath = os.path.join(output_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            print(f"Saved {filename}")

if __name__ == '__main__':
    import sys
    
    # Default to all pages if no max_pages specified
    max_pages = None
    if len(sys.argv) > 1:
        try:
            max_pages = int(sys.argv[1])
        except ValueError:
            print("Please provide a valid number of pages to scrape.")
            sys.exit(1)
    
    main('sitemap-webarticle-1.xml', max_pages)
