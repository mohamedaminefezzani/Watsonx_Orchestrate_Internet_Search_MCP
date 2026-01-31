# http_bridge.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import os

app = FastAPI()

class SearchRequest(BaseModel):
    query: str
    num_results: int = 5

class SearchResponse(BaseModel):
    results: str

@app.post("/search", response_model=SearchResponse)
async def search(request: SearchRequest):
    """HTTP endpoint that calls the MCP server"""
    try:
        server_params = StdioServerParameters(
            command="python3",
            args=["server.py"],
            env={"TAVILY_API_KEY": os.getenv("TAVILY_API_KEY")}
        )
        
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                
                result = await session.call_tool("web_search", {
                    "query": request.query,
                    "num_results": request.num_results
                })
                
                return SearchResponse(results=result.content[0].text)
                
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
