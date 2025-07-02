# Polymarket MCP Server

A **Model Context Protocol (MCP)** compliant server that exposes the public Polymarket Central Limit Order Book (CLOB) REST API as tools that any LLM-powered IDE or agent can invoke. Compatible with **Cursor**, **Continue** (VS Code), **GitHub Copilot Chat**, **JetBrains AI Assistant**, **OpenAI ChatGPT (Assistants API)**, **Smithery** and any other MCP-aware interface.

---

## ✨ Features

* 🪄 **Universal MCP Support** – works with Cursor, Continue, Copilot, JetBrains AI, Smithery and more
* ⚡ **Python implementation** – using native MCP protocol with async support
* 📈 **Essential endpoints out-of-the-box** – list markets, fetch single market details and more
* 🔌 **Stateless & no auth required** – queries Polymarket's public REST endpoints; no keys needed
* 🐳 **Docker-ready** – ship & deploy anywhere in seconds
* 📝 **MIT licensed** – free for personal and commercial use

---

## 🚀 Quick Start

### Local Development

```bash
# Clone the repository
git clone https://github.com/CarlosIbCu/polymarket-mcp.git
cd polymarket-mcp

# Install dependencies
pip install -r requirements.txt

# Run the server
python -m polymarket_mcp.main
```

### Testing with MCP Inspector

You can test the server using the official MCP Inspector:

```bash
# Install and run the MCP Inspector
npx @modelcontextprotocol/inspector python -m polymarket_mcp.main
```

This will:
1. Start the MCP server
2. Launch the inspector web interface
3. Provide a URL to access the inspector (usually http://localhost:6274)

The inspector allows you to:
- View available MCP tools
- Test tool calls interactively
- Inspect server capabilities
- Debug MCP protocol messages

### Docker Deployment

```bash
# Build the image
docker build -t polymarket-mcp .

# Run the container
docker run -p 3333:3333 polymarket-mcp
```

### Smithery Deployment

This server is ready for deployment on [Smithery](https://smithery.ai), the MCP hosting platform:

1. Fork/clone this repository
2. Connect your GitHub account to Smithery
3. Select this repository and choose "Custom Deploy"
4. Smithery will automatically detect the configuration and deploy

The `smithery.yaml` configuration includes:
- Container runtime settings
- Server configuration options
- Health checks
- Tool schemas

## 🛠 Available Tools

### `list_markets`
List available prediction markets with optional limit parameter.

**Parameters:**
- `limit` (integer, optional): Maximum number of markets to return (default: 10)

**Example:**
```json
{
  "limit": 5
}
```

### `get_market`
Fetch detailed information about a specific market.

**Parameters:**
- `market_id` (string, required): Market ID to fetch

**Example:**
```json
{
  "market_id": "0x9deb0baac40648821f96f01339229a422e2f5c877de55dc4dbf981f95a1e709c"
}
```

## 🔧 Configuration

Server configuration is handled via environment variables or Smithery config:

```yaml
server:
  host: "0.0.0.0"  # Server host
  port: 3333       # Server port
  timeout: 30      # Request timeout in seconds
```

## 📚 API Documentation

- **MCP Inspector**: Use `npx @modelcontextprotocol/inspector` for interactive testing
- **Polymarket API Docs**: [Official Documentation](https://docs.polymarket.com)

## 🧪 Testing

```bash
# Test the Polymarket API connectivity
python test_server.py

# Run with MCP Inspector for interactive testing
npx @modelcontextprotocol/inspector python -m polymarket_mcp.main
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is MIT licensed. See the [LICENSE](LICENSE) file for details.

---