# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **Model Context Protocol (MCP)** server that exposes Polymarket's public CLOB REST API as tools for LLM-powered IDEs and agents. The server is built with native MCP protocol implementation and provides a stateless interface to query prediction markets data.

## Development Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run the server locally
python -m polymarket_mcp.main

# Test with MCP Inspector
npx @modelcontextprotocol/inspector python -m polymarket_mcp.main

# Test API connectivity
python test_server.py

# Build Docker image
docker build -t polymarket-mcp .

# Run Docker container
docker run -p 3333:3333 polymarket-mcp
```

## Architecture

- **polymarket_mcp/main.py**: Core MCP server with native protocol implementation
- **polymarket_mcp/__init__.py**: Package version definition
- **smithery.yaml**: Smithery deployment configuration with health checks and tool schemas
- **Dockerfile**: Container configuration for deployment
- **test_server.py**: API connectivity test script

## MCP Implementation

The server uses native MCP protocol implementation:
- Direct JSON-RPC 2.0 message handling
- STDIO transport for standard MCP communication
- Manual protocol implementation for compatibility
- Async functions for tool execution

## MCP Tools

1. **list_markets**: Returns available prediction markets with optional limit parameter
2. **get_market**: Fetches detailed information for a specific market by ID

Both tools are implemented as async functions that make HTTP requests to the Polymarket CLOB API.

## External Dependencies

- Polymarket CLOB API base URL: `https://clob.polymarket.com`
- No authentication required (public endpoints only)
- Uses httpx for async HTTP requests to upstream API

## Key Features

- Native MCP protocol implementation for maximum compatibility
- Works with Python 3.8+ (no FastMCP dependency requirements)
- Direct JSON-RPC 2.0 message handling
- STDIO transport for standard MCP client integration
- Compatible with MCP Inspector for testing