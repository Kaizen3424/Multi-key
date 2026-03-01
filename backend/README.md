# AI Manus Backend

The backend service for AI Manus, built with FastAPI and Python.

## Architecture

The backend uses Domain-Driven Design (DDD) architecture:

```
backend/
├── app/
│   ├── application/     # Application services (orchestration)
│   ├── domain/          # Domain logic (agents, tools, prompts)
│   ├── infrastructure/  # External integrations (E2B, MongoDB, Redis)
│   │   └── external/
│   │       └── sandbox/    # E2B sandbox implementation
│   └── interfaces/     # API routes & dependencies
├── tests/              # Unit & integration tests
└── requirements.txt    # Python dependencies
```

## Requirements

- Python 3.9+
- MongoDB 4.4+
- Redis 6.0+
- E2B API key (get from https://e2b.dev/dashboard)

## Installation

1. **Create virtual environment:**
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# or .venv\Scripts\activate  # Windows
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Configure environment:**

Create a `.env` file:
```env
# Required: LLM API
API_KEY=your_llm_api_key
API_BASE=https://api.deepseek.com/v1
MODEL_NAME=deepseek-chat

# Required: E2B Sandbox
E2B_API_KEY=your_e2b_api_key

# Database
MONGODB_URI=mongodb://localhost:27017
REDIS_URL=redis://localhost:6379/0

# Auth (optional)
AUTH_PROVIDER=none
JWT_SECRET_KEY=your-secret-key
```

## Running

### Development
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Production
```bash
# Using the run script
./run.sh

# Or directly
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

## E2B Sandbox

The backend uses E2B cloud sandboxes for code execution. Each agent session gets its own isolated E2B sandbox.

### Configuration

| Variable | Description | Default |
|----------|-------------|---------|
| `E2B_API_KEY` | Your E2B API key | Required |
| `E2B_TEMPLATE` | Sandbox template | `base` |
| `E2B_TIMEOUT` | Execution timeout (seconds) | 300 |

### Available Templates

- `base` - Basic environment
- `python` - Python development
- `nodejs` - Node.js development
- `rust` - Rust development

## API Endpoints

### Base URL
`/api/v1`

### Core Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| PUT | `/api/v1/sessions` | Create session |
| GET | `/api/v1/sessions` | List sessions |
| GET | `/api/v1/sessions/{id}` | Get session |
| DELETE | `/api/v1/sessions/{id}` | Delete session |
| POST | `/api/v1/sessions/{id}/chat` | Send message (SSE) |
| POST | `/api/v1/sessions/{id}/stop` | Stop session |

### Tool Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/sessions/{id}/shell` | View shell output |
| POST | `/api/v1/sessions/{id}/file` | View file content |

### WebSocket

- `/api/v1/sessions/{id}/vnc` - Browser VNC (if supported)

## Testing

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_sandbox_file.py

# Run with coverage
pytest --cov=app tests/
```

## Project Structure

### Domain Layer (`app/domain/`)

- `models/` - Domain models (Session, Message, ToolResult)
- `services/` - Domain services (Agent, Planner, Execution)
- `external/` - External interfaces (Sandbox)
- `prompts/` - LLM prompt templates

### Application Layer (`app/application/`)

- `services/` - Application services (AgentService, FileService, AuthService)
- `schemas/` - Request/Response schemas

### Infrastructure Layer (`app/infrastructure/`)

- `external/` - External service implementations
  - `sandbox/` - E2B sandbox client
  - `llm/` - LLM client (OpenAI, DeepSeek)
  - `cache/` - Redis cache
  - `file/` - File storage (GridFS)
- `repositories/` - Data access (MongoDB repositories)

### Interfaces Layer (`app/interfaces/`)

- `api/` - FastAPI routes
- `dependencies.py` - Dependency injection

## License

MIT
