# server.py
from mcp.server.fastmcp import FastMCP
import os
import requests

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

server = FastMCP("search-mcp")

@server.tool()
async def web_search(query: str, num_results: int = 5) -> str:
    """Search the web using Tavily
    
    Args:
        query: The search query
        num_results: Number of results to return (default: 5)
    
    Returns:
        Search results with titles and links
    """
    if not TAVILY_API_KEY:
        return "Error: TAVILY_API_KEY not set"
    
    try:
        response = requests.post(
            "https://api.tavily.com/search",
            json={
                "api_key": TAVILY_API_KEY,
                "query": query,
                "max_results": num_results
            }
        )
        response.raise_for_status()
        data = response.json()
        
        results = data.get("results", [])
        if not results:
            return "No results found"
        
        output = []
        for i, r in enumerate(results, 1):
            title = r.get('title', 'No title')
            url = r.get('url', 'No link')
            content = r.get('content', '')
            output.append(f"{i}. {title}\n   {url}\n   {content}\n")
        
        return "\n".join(output)
        
    except Exception as e:
        return f"Search failed: {str(e)}"

if __name__ == "__main__":
    server.run()
