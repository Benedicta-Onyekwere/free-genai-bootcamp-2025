"""Tool for searching the web using SERP API."""

import os
from typing import List, Dict, Optional
import aiohttp
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key from environment
SERP_API_KEY = os.getenv('SERP_API_KEY')

async def search_web_serp(query: str, max_results: int = 5) -> List[Dict[str, str]]:
    """Search the web for song lyrics using SERP API.
    
    Args:
        query: Search query (song title + artist + "lyrics")
        max_results: Maximum number of search results to return
        
    Returns:
        List of search results with title and link
    """
    if not SERP_API_KEY:
        print("SERP API key not found in environment variables")
        return []
        
    # Add "lyrics" to query if not present
    if "lyrics" not in query.lower():
        query = f"{query} lyrics"
    
    # SERP API endpoint
    url = "https://serpapi.com/search"
    
    # Parameters for the API request
    params = {
        "api_key": SERP_API_KEY,
        "engine": "google",
        "q": query,
        "num": max_results,
        "gl": "jp"  # Set region to Japan for better Japanese results
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    # Extract organic search results
                    results = []
                    if "organic_results" in data:
                        for result in data["organic_results"][:max_results]:
                            results.append({
                                "title": result.get("title", ""),
                                "link": result.get("link", ""),
                                "snippet": result.get("snippet", "")
                            })
                    return results
                else:
                    print(f"Error: SERP API returned status code {response.status}")
                    return []
                    
    except Exception as e:
        print(f"Error searching with SERP API: {e}")
        return [] 