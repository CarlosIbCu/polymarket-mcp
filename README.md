# Polymarket MCP Server

A **Model Context Protocol (MCP)** compliant server that exposes the public Polymarket Central Limit Order Book (CLOB) REST API as tools that any LLM-powered IDE or agent can invoke. Compatible with **Cursor**, **Continue** (VS Code), **GitHub Copilot Chat**, **JetBrains AI Assistant**, **OpenAI ChatGPT (Assistants API)**, **Smithery** and any other MCP-aware interface.

---

## ✨ Features

* 🪄 **Universal MCP Support** – works with Cursor, Continue, Copilot, JetBrains AI, Smithery and more
* ⚡ **FastAPI powered** – an async Python implementation capable of thousands of requests / second
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
uvicorn polymarket_mcp.main:app --host 0.0.0.0 --port 3333 --reload
```

The server will be available at:
- OpenAPI docs: http://localhost:3333/docs
- MCP schema: http://localhost:3333/schema or http://localhost:3333/mcp

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

### List Markets
```typescript
GET /markets
// List available prediction markets with optional limit
```

### Get Market Details
```typescript
GET /markets/{market_id}
// Fetch detailed information about a specific market
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

- **OpenAPI/Swagger UI**: Available at `/docs` when running locally
- **MCP Schema**: Available at `/schema` or `/mcp`
- **Polymarket API Docs**: [Official Documentation](https://docs.polymarket.com)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is MIT licensed. See the [LICENSE](LICENSE) file for details.

---

Made with ❤️ for the Model Context Protocol community 