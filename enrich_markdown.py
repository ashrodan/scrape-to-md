import os
import re
import argparse
from typing import List, Dict
import frontmatter
from openai import OpenAI

def read_markdown_files(directory: str = None, specific_file: str = None) -> List[Dict]:
    """Read markdown files from a directory or a specific file."""
    markdown_files = []
    
    if specific_file:
        # If a specific file is provided, read only that file
        if not specific_file.endswith('.md'):
            raise ValueError("The specified file must be a markdown file (.md)")
        
        if not os.path.exists(specific_file):
            raise FileNotFoundError(f"File not found: {specific_file}")
        
        with open(specific_file, 'r', encoding='utf-8') as f:
            post = frontmatter.load(f)
            markdown_files.append({
                'filepath': specific_file,
                'filename': os.path.basename(specific_file),
                'metadata': post.metadata,
                'content': post.content
            })
    else:
        # If no specific file, read all markdown files in the directory
        directory = directory or 'articles'
        for filename in os.listdir(directory):
            if filename.endswith('.md'):
                filepath = os.path.join(directory, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    post = frontmatter.load(f)
                    markdown_files.append({
                        'filepath': filepath,
                        'filename': filename,
                        'metadata': post.metadata,
                        'content': post.content
                    })
    
    return markdown_files

def generate_metadata_with_openai(content: str, client: OpenAI) -> Dict[str, str]:
    """Generate summary and keywords using OpenAI."""
    try:
        # Generate summary
        summary_response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that generates concise summaries."},
                {"role": "user", "content": f"Generate a short, professional, no fluff summary (max 100 words) for this text:\n\n{content}"}
            ]
        )
        summary = summary_response.choices[0].message.content.strip()

        # Generate keywords
        keywords_response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that extracts key themes and keywords."},
                {"role": "user", "content": f"Extract 5-7 key themes or keywords from this text:\n\n{content}"}
            ]
        )
        keywords = keywords_response.choices[0].message.content.strip().split('\n')
        keywords = [kw.strip('- ') for kw in keywords]

        return {
            'summary': summary,
            'keywords': keywords
        }
    except Exception as e:
        print(f"Error generating metadata: {e}")
        return {
            'summary': 'Unable to generate summary',
            'keywords': []
        }

def update_markdown_files(markdown_files: List[Dict], client: OpenAI):
    """Update markdown files with new metadata."""
    for file in markdown_files:
        # Generate new metadata
        new_metadata = generate_metadata_with_openai(file['content'], client)
        
        # Update file metadata
        file['metadata']['summary'] = new_metadata['summary']
        file['metadata']['keywords'] = new_metadata['keywords']
        
        # Write updated file
        post = frontmatter.Post(file['content'], **file['metadata'])
        with open(file['filepath'], 'wb') as f:
            frontmatter.dump(post, f)
        
        print(f"Updated {file['filename']}:")
        print(f"Summary: {new_metadata['summary']}")
        print(f"Keywords: {new_metadata['keywords']}\n")

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Enrich markdown files with AI-generated metadata')
    parser.add_argument('-f', '--file', help='Path to a specific markdown file to enrich', default=None)
    parser.add_argument('-d', '--directory', help='Directory containing markdown files (default: articles)', default='articles')
    args = parser.parse_args()

    # Ensure OpenAI API key is set
    import os
    if 'OPENAI_API_KEY' not in os.environ:
        raise ValueError("Please set the OPENAI_API_KEY environment variable")
    
    # Initialize OpenAI client
    client = OpenAI()
    
    # Read markdown files
    markdown_files = read_markdown_files(args.directory, args.file)
    
    # Update files with new metadata
    update_markdown_files(markdown_files, client)

if __name__ == '__main__':
    main()
