import requests
from bs4 import BeautifulSoup

def debug_html_structure(url):
    """Detailed HTML structure debugging."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        print("=== HTML STRUCTURE DEBUGGING ===")
        print(f"URL: {url}")
        
        # Find all divs
        print("\n--- All DIV Elements ---")
        divs = soup.find_all('div')
        for div in divs:
            print(f"DIV Classes: {div.get('class')}")
            div_attrs = div.attrs
            print(f"DIV Attributes: {div_attrs}")
            print("---")
        
        # Find potential article body divs
        print("\n--- Potential Article Body Divs ---")
        potential_bodies = soup.find_all('div', class_='knowledgeArticle')
        for body in potential_bodies:
            print("Found knowledgeArticle div:")
            print(body.prettify()[:500])  # First 500 chars
        
        # Find lightning-formatted-rich-text elements
        print("\n--- Lightning Formatted Rich Text Elements ---")
        rich_texts = soup.find_all('lightning-formatted-rich-text')
        for text in rich_texts:
            print(text.prettify()[:500])  # First 500 chars
        
    except Exception as e:
        print(f"Error debugging {url}: {e}")

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Please provide a URL to debug")
        sys.exit(1)
    
    debug_html_structure(sys.argv[1])
