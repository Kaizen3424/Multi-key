# 🚀 Quick Start

## Environment Requirements

This project requires:

- **Docker** (for running backend, MongoDB, Redis)
- **Docker Compose** 

Model capabilities required:

- Compatible with OpenAI API
- Supports Function Call
- Supports JSON Format output

Recommended models: Deepseek and ChatGPT.

## E2B Setup

AI Manus uses E2B cloud sandboxes. Get your free API key:

1. Go to https://e2b.dev/dashboard
2. Sign up and get your API key
3. Set `E2B_API_KEY` environment variable

## Deployment

Deploy using Docker Compose:

```bash
# Copy environment file
cp .env.example .env

# Edit .env with your API keys
nano .env

# Start services
docker compose up -d
```

> Note: You need to set both `API_KEY` (for LLM) and `E2B_API_KEY` (for sandbox) in .env

Open your browser and visit <http://localhost:5173> to access Manus.

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `API_KEY` | Yes | Your LLM API key (OpenAI, DeepSeek, etc.) |
| `E2B_API_KEY` | Yes | Your E2B API key from https://e2b.dev/dashboard |
| `API_BASE` | No | LLM API base URL (default: https://api.deepseek.com/v1) |
| `MODEL_NAME` | No | Model name (default: deepseek-chat) |
| `AUTH_PROVIDER` | No | Auth type: none, password, local (default: none) |
