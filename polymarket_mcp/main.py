#!/usr/bin/env python3
"""Simple MCP server for Polymarket using basic MCP protocol."""

import asyncio
import json
import sys
from typing import Any, Dict, Optional
import httpx

BASE_URL = "https://clob.polymarket.com"

async def list_markets(limit: Optional[int] = 10) -> Dict[str, Any]:
    """List available prediction markets."""
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(f"{BASE_URL}/markets", params={"limit": limit})
        response.raise_for_status()
        return response.json()

async def get_market(market_id: str) -> Dict[str, Any]:
    """Get details for a specific market."""
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(f"{BASE_URL}/markets/{market_id}")
        response.raise_for_status()
        return response.json()

async def handle_request(request: Dict[str, Any]) -> Dict[str, Any]:
    """Handle MCP request."""
    method = request.get("method")
    params = request.get("params", {})
    request_id = request.get("id")
    
    # Handle notification methods (no response needed)
    if method == "notifications/initialized":
        return None
    
    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {}
                },
                "serverInfo": {
                    "name": "polymarket-mcp-server",
                    "version": "0.1.0"
                }
            }
        }
    
    elif method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "tools": [
                    {
                        "name": "list_markets",
                        "description": "List available prediction markets",
                        "inputSchema": {
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
                        "inputSchema": {
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
        }
    
    elif method == "tools/call":
        tool_name = params.get("name")
        arguments = params.get("arguments", {})
        
        try:
            if tool_name == "list_markets":
                result = await list_markets(arguments.get("limit", 10))
            elif tool_name == "get_market":
                result = await get_market(arguments["market_id"])
            else:
                raise ValueError(f"Unknown tool: {tool_name}")
            
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": json.dumps(result, indent=2)
                        }
                    ]
                }
            }
        except Exception as e:
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {
                    "code": -32000,
                    "message": str(e)
                }
            }
    
    else:
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {
                "code": -32601,
                "message": f"Method not found: {method}"
            }
        }

async def main():
    """Run the MCP server using stdio transport."""
    while True:
        try:
            line = await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)
            if not line:
                break
            
            line = line.strip()
            if not line:
                continue
                
            request = json.loads(line)
            response = await handle_request(request)
            
            # Only send response if it's not None (for notifications)
            if response is not None:
                print(json.dumps(response), flush=True)
            
        except json.JSONDecodeError:
            continue
        except Exception as e:
            error_response = {
                "jsonrpc": "2.0",
                "id": request.get("id") if 'request' in locals() else None,
                "error": {
                    "code": -32700,
                    "message": f"Parse error: {str(e)}"
                }
            }
            print(json.dumps(error_response), flush=True)

if __name__ == "__main__":
    asyncio.run(main())