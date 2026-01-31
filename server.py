from mcp.server import Server
from mcp.server.stdio import stdio_server
from utils import get_google_api_keys
from langchain_google_community import GoogleSearchAPIWrapper

from dotenv import load_dotenv
load_dotenv()

search = GoogleSearchAPIWrapper(
    google_api_key=GOOGLE_API_KEY,
    google_cse_id=GOOGLE_CSE_ID,
    k=5
)

server = Server("google-search-mcp")

@server.list_tools()
async def list_tools():
    return [{
        "name": "google_search",
        "description": "Search the web using Google",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string"},
                "num_results": {"type": "integer", "default": 5}
            },
            "required": ["query"]
        }
    }]

@server.call_tool()
async def call_tool(name, arguments):
    if name != "google_search":
        raise ValueError("Unknown tool")

    query = arguments["query"]
    k = arguments.get("num_results", 5)

    results = search.results(query, num_results=k)

    return {
        "content": [{
            "type": "text",
            "text": "\n".join(
                f"{r['title']} — {r['link']}"
                for r in results
            )
        }]
    }

if __name__ == "__main__":
    stdio_server(server)

