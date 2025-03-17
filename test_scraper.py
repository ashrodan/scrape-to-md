from bs4 import BeautifulSoup

def extract_text_from_rich_text(soup_element):
    """Extract clean text from lightning-formatted-rich-text elements."""
    texts = []
    for paragraph in soup_element.find_all('p'):
        # Find all span elements within the paragraph
        spans = paragraph.find_all('span', attrs={'lwc-4nfn2rc40ch': ''})
        para_text = ' '.join([span.get_text(strip=True) for span in spans if span.get_text(strip=True)])
        if para_text:
            texts.append(para_text)
    return '\n\n'.join(texts)

def test_parsing():
    with open('sample.html', 'r') as f:
        html_content = f.read()
    
    soup = BeautifulSoup(html_content, 'html.parser')
    article_body = soup.find('div', attrs={'articlebody-articlebody_articlebody': True, 'class': 'knowledgeArticle'})
    
    # Extract titles
    titles = article_body.find_all('h2')
    print("Titles:")
    for title in titles:
        print(title.get_text(strip=True))
    
    # Extract content
    content = extract_text_from_rich_text(article_body)
    print("\nContent:")
    print(content)

if __name__ == '__main__':
    test_parsing()
