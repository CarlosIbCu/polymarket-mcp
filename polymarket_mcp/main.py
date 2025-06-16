from fastapi import FastAPI, Query, HTTPException
from typing import Optional
import httpx

app = FastAPI(
    title="Polymarket MCP Server",
    description="Model Context Protocol server exposing Polymarket CLOB REST endpoints as LLM tools.",
    version="0.1.0",
)

BASE_URL = "https://clob.polymarket.com"


@app.get("/schema", tags=["mcp"])
async def get_schema():
    """Return the MCP schema so IDEs like Cursor can auto-register the tools."""
    return {
        "schema_version": 1,
        "name_for_model": "PolymarketMCP",
        "name_for_human": "Polymarket API",
        "description_for_model": (
            "Tooling for fetching market data from the Polymarket Central Limit Order Book. "
            "Useful for prediction market insights."
        ),
        "description_for_human": "Query prediction markets, prices and books from Polymarket.",
        "auth": {"type": "none"},
        "api": {
            "type": "openapi",
            "url": "/openapi.json",
        },
        "contact_email": "support@polymarket.com",
        "legal_info_url": "https://polymarket.com/legal",
    }


@app.get(
    "/markets",
    tags=["markets"],
    summary="List Polymarket markets (paginated)",
    description="Returns a paginated list of available markets from the Polymarket CLOB REST API.",
)
async def get_markets(next_cursor: Optional[str] = Query("", description="Pagination cursor")):
    params = {"next_cursor": next_cursor} if next_cursor else None
    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.get(f"{BASE_URL}/markets", params=params)
    if response.status_code != 200:
        raise HTTPException(status_code=502, detail="Failed to fetch markets from Polymarket")
    return response.json()


@app.get(
    "/markets/{condition_id}",
    tags=["markets"],
    summary="Get single market details",
    description="Fetch data for a single market by its condition_id.",
)
async def get_market(condition_id: str):
    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.get(f"{BASE_URL}/markets/{condition_id}")
    if response.status_code != 200:
        raise HTTPException(status_code=502, detail="Failed to fetch market data from Polymarket")
    return response.json() 