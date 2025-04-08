import httpx
from bs4 import BeautifulSoup
from typing import Optional
import re

async def get_page_content(url: str) -> Optional[str]:
    """
    Fetch and extract the main content from a webpage.
    
    Args:
        url (str): URL of the webpage to fetch
        
    Returns:
        Optional[str]: Extracted text content or None if failed
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, follow_redirects=True)
            response.raise_for_status()
            
            # Parse HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove script and style elements
            for element in soup(['script', 'style', 'header', 'footer', 'nav']):
                element.decompose()
            
            # Get text content
            text = soup.get_text()
            
            # Clean up text
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = '\n'.join(chunk for chunk in chunks if chunk)
            
            # Basic cleanup
            text = re.sub(r'\n\s*\n', '\n\n', text)  # Remove multiple newlines
            text = re.sub(r'[\t\r\f\v]', ' ', text)  # Replace tabs and other whitespace
            text = re.sub(r'\s+', ' ', text)         # Replace multiple spaces
            
            return text.strip()
            
    except Exception as e:
        print(f"Error fetching page content: {e}")
        return None 