# AI Manus

[![GitHub stars](https://img.shields.io/github/stars/simpleyyt/ai-manus?style=social)](https://github.com/simpleyyt/ai-manus/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

AI Manus is a general-purpose AI Agent system that supports running various tools and operations in an isolated E2B cloud sandbox environment.

🚀 [Try a Demo](https://app.ai-manus.com)

## Demos

### Basic Features

https://github.com/user-attachments/assets/37060a09-c647-4bcb-920c-959f7fa73ebe

### Browser Use

*Task: Latest LLM papers*

https://github.com/user-attachments/assets/4e35bc4d-024a-4617-8def-a537a94bd285

### Code Use

*Task: Write a complex Python example*

https://github.com/user-attachments/assets/765ea387-bb1c-4dc2-b03e-716698feef77

## Key Features

- **E2B Cloud Sandbox**: All code execution runs in isolated E2B cloud containers
- **Multi-Tool Support**: Terminal, Browser, File operations, Web Search
- **MCP Integration**: Supports external MCP (Model Context Protocol) tools
- **Session Management**: Persistent conversations with MongoDB
- **Real-time Execution**: Live streaming of agent progress via WebSocket
- **Authentication**: User login and session management

## Architecture

```
┌─────────────┐     ┌─────────────┐     ┌──────────────────┐
│  Frontend   │────▶│   Backend   │────▶│   E2B Sandbox    │
│  (React)    │     │  (FastAPI)  │     │   (Cloud)        │
└─────────────┘     └─────────────┘     └──────────────────┘
                           │                     │
                           ▼                     ▼
                    ┌─────────────┐       ┌─────────────┐
                    │  MongoDB    │       │   Browser   │
                    │  (Sessions) │       │   Terminal  │
                    └─────────────┘       └─────────────┘
```

## Quick Start

### Prerequisites

- **LLM API Key**: OpenAI, DeepSeek, or compatible API
- **E2B API Key**: Get from [e2b.dev/dashboard](https://e2b.dev/dashboard)
- **Docker** (optional, for local MongoDB/Redis)

### Option 1: Local Development with Docker

1. **Clone the repository:**
```bash
git clone https://github.com/simpleyyt/ai-manus.git
cd ai-manus
```

2. **Create environment file:**
```bash
cp .env.example .env
```

3. **Configure your API keys in `.env`:**
```env
# Required: Your LLM API
API_KEY=your_llm_api_key_here
API_BASE=https://api.deepseek.com/v1  # or OpenAI URL
MODEL_NAME=deepseek-chat

# Required: E2B Sandbox API key
E2B_API_KEY=your_e2b_api_key_here
```

4. **Start the services:**
```bash
# Using Docker Compose
docker-compose -f docker-compose.yml up -d
```

5. **Access the application:**
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000

### Option 2: Local Development (No Docker)

For the backend, you can run directly on your machine:

1. **Install Python dependencies:**
```bash
cd backend
pip install -r requirements.txt
```

2. **Configure environment:**
```bash
export API_KEY=your_llm_api_key
export E2B_API_KEY=your_e2b_api_key
export MONGODB_URI=mongodb://localhost:27017
export REDIS_URL=redis://localhost:6379/0
```

3. **Start the backend:**
```bash
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

4. **Start the frontend:**
```bash
cd frontend
npm install
npm run dev
```

## Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `API_KEY` | LLM API key (OpenAI/DeepSeek) | Yes | - |
| `API_BASE` | LLM API base URL | No | `https://api.deepseek.com/v1` |
| `MODEL_NAME` | LLM model name | No | `deepseek-chat` |
| `E2B_API_KEY` | E2B Sandbox API key | Yes | - |
| `E2B_TEMPLATE` | E2B sandbox template | No | `base` |
| `E2B_TIMEOUT` | Execution timeout (seconds) | No | `300` |
| `MONGODB_URI` | MongoDB connection string | No | `mongodb://mongodb:27017` |
| `REDIS_URL` | Redis connection URL | No | `redis://redis:6379/0` |
| `AUTH_PROVIDER` | Auth method: `password`, `none`, `local` | No | `password` |
| `JWT_SECRET_KEY` | JWT signing key | No | `your-secret-key-here` |

### E2B Templates

Available E2B sandbox templates:
- `base` - Basic environment with common tools
- `python` - Python development environment
- `nodejs` - Node.js development environment
- `rust` - Rust development environment
- And more...

## Configuration Examples

### Using OpenAI

```env
API_KEY=sk-xxxxxxxxxxxxxxxx
API_BASE=https://api.openai.com/v1
MODEL_NAME=gpt-4o
E2B_API_KEY=e2b_xxxxxxxxxxxxxxxx
```

### Using DeepSeek

```env
API_KEY=sk-xxxxxxxxxxxxxxxx
API_BASE=https://api.deepseek.com/v1
MODEL_NAME=deepseek-chat
E2B_API_KEY=e2b_xxxxxxxxxxxxxxxx
```

## Development Guide

### Project Structure

```
ai-manus/
├── frontend/           # React frontend application
├── backend/           # FastAPI backend application
│   ├── app/
│   │   ├── application/    # Application services
│   │   ├── domain/          # Domain logic & agents
│   │   ├── infrastructure/  # External integrations (E2B, MongoDB, Redis)
│   │   └── interfaces/      # API routes & dependencies
│   └── tests/               # Unit & integration tests
├── project.md         # Detailed project documentation
└── docker-compose*.yml
```

### Running Tests

```bash
cd backend
pip install pytest pytest-asyncio
pytest tests/
```

### API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Troubleshooting

### E2B Sandbox Issues

1. **"E2B_API_KEY is required"**: Make sure you've set the `E2B_API_KEY` environment variable
2. **Sandbox timeout**: Increase `E2B_TIMEOUT` in your configuration
3. **Template not found**: Ensure you're using a valid E2B template name

### MongoDB/Redis Issues

1. **Connection refused**: Ensure MongoDB and Redis are running
2. **Use Docker**: The easiest way is to run them via Docker:
   ```bash
   docker run -d -p 27017:27017 mongo:7.0
   docker run -d -p 6379:6379 redis:7.0
   ```

## Documentation

For detailed documentation, see [project.md](project.md):
- Architecture overview
- How it works
- Component details
- Security considerations
- Technology stack

## License

MIT License - See [LICENSE](LICENSE) for details.

## Support

- Documentation: [docs.ai-manus.com](https://docs.ai-manus.com)
- Demo: [app.ai-manus.com](https://app.ai-manus.com)
- GitHub: [github.com/simpleyyt/ai-manus](https://github.com/simpleyyt/ai-manus)

---

⭐️ Star us on GitHub if you find this project useful!
