from fastapi import FastAPI, Query, HTTPException, Request
from typing import Optional, Dict, Any
import httpx
import json

app = FastAPI(
    title="Polymarket MCP Server",
    description="Model Context Protocol server exposing Polymarket CLOB REST endpoints as LLM tools.",
    version="0.1.0",
)

BASE_URL = "https://clob.polymarket.com"

async def get_mcp_schema():
    """Return the MCP schema in Smithery's expected format."""
    return {
        "schema_version": 1,
        "name_for_model": "PolymarketMCP",
        "name_for_human": "Polymarket API",
        "description_for_model": (
            "Tooling for fetching market data from the Polymarket Central Limit Order Book. "
            "Useful for prediction market insights."
        ),
        "description_for_human": "Query prediction markets data from Polymarket's CLOB API.",
        "tools": [
            {
                "name": "list_markets",
                "description": "List available prediction markets",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "limit": {
                            "type": "integer",
                            "description": "Maximum number of markets to return",
                            "default": 10
                        }
                    }
                }
            },
            {
                "name": "get_market",
                "description": "Get details for a specific market",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "market_id": {
                            "type": "string",
                            "description": "Market ID to fetch"
                        }
                    },
                    "required": ["market_id"]
                }
            }
        ]
    }

@app.get("/mcp")
@app.post("/mcp")
@app.delete("/mcp")
async def handle_mcp(request: Request):
    """Handle Smithery MCP requests with configuration."""
    try:
        # Parse dot-notation query params into config object
        config = {}
        for key, value in request.query_params.items():
            parts = key.split('.')
            current = config
            for part in parts[:-1]:
                current = current.setdefault(part, {})
            current[parts[-1]] = value
        
        # Return schema on GET
        if request.method == "GET":
            return await get_mcp_schema()
            
        # Handle POST for tool invocation
        if request.method == "POST":
            body = await request.json()
            tool_name = body.get("name")
            parameters = body.get("parameters", {})
            
            if tool_name == "list_markets":
                limit = parameters.get("limit", 10)
                return await list_markets(limit)
            elif tool_name == "get_market":
                market_id = parameters.get("market_id")
                if not market_id:
                    raise HTTPException(status_code=400, detail="market_id is required")
                return await get_market(market_id)
            else:
                raise HTTPException(status_code=400, detail=f"Unknown tool: {tool_name}")
                
        # DELETE for cleanup (no-op in our case)
        if request.method == "DELETE":
            return {"status": "success"}
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/schema", tags=["mcp"])
async def get_schema():
    """Return the MCP schema so IDEs like Cursor can auto-register the tools."""
    return await get_mcp_schema()

@app.get("/markets")
async def list_markets(
    limit: Optional[int] = Query(10, description="Maximum number of markets to return")
) -> Dict[str, Any]:
    """List available prediction markets."""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/markets", params={"limit": limit})
        response.raise_for_status()
        return response.json()

@app.get("/markets/{market_id}")
async def get_market(
    market_id: str = Query(..., description="Market ID to fetch")
) -> Dict[str, Any]:
    """Get details for a specific market."""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/markets/{market_id}")
        response.raise_for_status()
        return response.json() 