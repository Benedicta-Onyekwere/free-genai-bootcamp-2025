from duckduckgo_search import DDGS
from typing import List, Dict
import asyncio
from functools import partial

async def search_web_ddg(query: str, max_results: int = 5) -> List[Dict[str, str]]:
    """
    Search the web for song lyrics using DuckDuckGo.
    
    Args:
        query (str): Search query (song title + artist + "lyrics")
        max_results (int): Maximum number of search results to return
        
    Returns:
        List[Dict[str, str]]: List of search results with title and link
    """
    # Add "lyrics" to the search query if not present
    if "lyrics" not in query.lower():
        query = f"{query} lyrics"
        
    try:
        # Run DuckDuckGo search in a thread pool since it's synchronous
        loop = asyncio.get_event_loop()
        search_func = partial(DDGS().text, query, max_results=max_results)
        results = await loop.run_in_executor(None, search_func)
        
        # Convert results to list of dictionaries
        formatted_results = []
        for result in results:
            formatted_results.append({
                "title": result["title"],
                "link": result["link"],
                "snippet": result["body"]
            })
            
        return formatted_results
        
    except Exception as e:
        print(f"Error searching web: {e}")
        return [] 