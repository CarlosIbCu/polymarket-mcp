# Polymarket MCP Server

A **Model Context Protocol (MCP)** compliant server that exposes the public Polymarket Central Limit Order Book (CLOB) REST API as tools that any LLM-powered IDE or agent can invoke. Compatible with **Cursor**, **Continue** (VS Code), **GitHub Copilot Chat**, **JetBrains AI Assistant**, **OpenAI ChatGPT (Assistants API)** and any other MCP-aware interface.

---

## ✨ Features

* 🪄 **Plug-and-play with Cursor** – point Cursor to the running server's `/schema` endpoint and start querying Polymarket data straight from your chat.
* ⚡ **FastAPI powered** – an async Python implementation capable of thousands of requests / second.
* 📈 **Essential endpoints out-of-the-box** – list markets, fetch single market details and more.
* 🔌 **Stateless & no auth required** – queries Polymarket's public REST endpoints; no keys needed.
* 🐳 **Docker-ready** – ship & deploy anywhere in seconds.
* 📝 **MIT licensed** – free for personal and commercial use.

---

## 🚀 Quick start

```bash
# 1. Clone repository
$ git clone https://github.com/<your-user>/polymarket-mcp.git && cd polymarket-mcp

# 2. Install dependencies (Python ≥ 3.9)
$ python -m venv venv && source venv/bin/activate
$ pip install -r requirements.txt

# 3. Run the server
$ uvicorn polymarket_mcp.main:app --reload --port 3333

# 4. Point Cursor to http://localhost:3333/schema
```

You can now ask the LLM:

> "List the first 10 active Polymarket markets"

and it will automatically call the `get_markets` tool behind the scenes.

---

## 🛠️ Endpoints

| Route | Description |
|-------|-------------|
| `GET /schema` | MCP schema consumed by Cursor |
| `GET /markets` | Paginated Polymarket markets (`next_cursor` query param) |
| `GET /markets/{condition_id}` | Single market details |

---

## 🌐 Deployment

### Docker

```bash
# Build and run
$ docker build -t polymarket-mcp .
$ docker run -d -p 3333:3333 polymarket-mcp
```

### Vercel / Fly.io / Render

The server is a standard ASGI app – deploy it as you would any FastAPI service.

---

## 🔍 SEO Keywords

polymarket • model context protocol • mcp server • prediction markets api • llm tools • fastapi • polymarket clob • ai plugin

---

## 📄 License

[MIT](LICENSE) 