FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY polymarket_mcp/ polymarket_mcp/

EXPOSE 3333

CMD ["sh", "-c", "uvicorn polymarket_mcp.main:app --host 0.0.0.0 --port ${PORT:-3333}"] 