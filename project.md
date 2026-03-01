# AI Manus - Project Documentation

## Table of Contents
1. [Project Overview](#project-overview)
2. [What is AI Manus?](#what-is-ai-manus)
3. [Architecture](#architecture)
4. [How It Works](#how-it-works)
5. [Key Components](#key-components)
6. [Sandbox System](#sandbox-system)
7. [Technology Stack](#technology-stack)

---

## Project Overview

AI Manus is a general-purpose AI Agent system that can execute various tools and operations within a sandboxed environment. It leverages Large Language Models (LLMs) to understand user requests and orchestrates tool execution to accomplish complex tasks.

### Key Characteristics

- **Autonomous Agent**: AI Manus can plan, execute, and iterate on tasks autonomously
- **Sandbox Execution**: All code and browser operations run in isolated E2B cloud sandboxes
- **Multi-tool Support**: Terminal, Browser, File operations, Web Search, and external MCP tools
- **Session Management**: Persistent conversations with MongoDB and background task support
- **Authentication**: User login and session management

---

## What is AI Manus?

AI Manus (Manus = "Hand" in Latin) is an AI assistant that can work autonomously on your behalf. Unlike traditional chatbots that simply respond to queries, AI Manus can:

- **Execute Code**: Run Python, JavaScript, and other languages in isolated sandboxes
- **Browse the Web**: Navigate websites, fill forms, and extract information
- **Manage Files**: Create, read, upload, and download files
- **Run Terminal Commands**: Execute shell commands for system operations
- **Search the Web**: Find information using search engines

### Use Cases

1. **Data Analysis**: Analyze datasets, generate visualizations
2. **Research**: Find and summarize information from the web
3. **Automation**: Automate repetitive browser tasks
4. **Code Development**: Write, test, and debug code
5. **Content Creation**: Generate documents, reports, presentations

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         Frontend                                 │
│                    (React + TypeScript)                         │
│                      http://localhost:5173                      │
└─────────────────────────┬─────────────────────────────────────────┘
                          │
                          │ HTTP/WebSocket
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                         Backend                                  │
│                    (FastAPI + Python)                           │
│                      http://localhost:8000                      │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐ │
│  │   Agent     │  │   Auth      │  │    Session Manager      │ │
│  │   Service   │  │   Service   │  │                         │ │
│  └─────────────┘  └─────────────┘  └─────────────────────────┘ │
└─────────────────────────┬─────────────────────────────────────────┘
                          │
                          │ API Calls
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                    E2B Cloud Sandbox                             │
│              (Code Execution & Browser Automation)              │
│                                                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐│
│  │   Terminal  │  │   Browser   │  │    File System          ││
│  │   Tool      │  │   Tool      │  │    Tool                 ││
│  └─────────────┘  └─────────────┘  └─────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
                          │
          ┌───────────────┼───────────────┐
          ▼               ▼               ▼
    ┌──────────┐   ┌──────────┐   ┌──────────┐
    │ MongoDB   │   │  Redis   │   │   LLM    │
    │(Sessions) │   │ (Tasks)  │   │(OpenAI/  │
    └──────────┘   └──────────┘   │ DeepSeek)│
                                   └──────────┘
```

---

## How It Works

### 1. User Request Flow

1. **User Input**: User sends a request through the web interface
2. **Session Creation**: Backend creates or retrieves an existing session
3. **Agent Initialization**: Agent service initializes with LLM and tools
4. **Planning**: Agent breaks down the task into steps
5. **Execution**: Agent executes each step using appropriate tools
6. **Feedback**: Results are streamed back to the user in real-time

### 2. Tool Execution Flow

```
User Request
     │
     ▼
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Planner   │────▶│  Execution  │────▶│   Result    │
│   Agent     │     │   Agent     │     │   Parser    │
└─────────────┘     └─────────────┘     └─────────────┘
      │                   │
      │            ┌──────┴──────┐
      │            ▼             ▼
      │     ┌──────────┐  ┌──────────┐
      │     │ Terminal │  │ Browser  │
      │     │  Tool    │  │  Tool    │
      │     └──────────┘  └──────────┘
      │            │
      │            ▼
      │     ┌──────────┐
      └────▶│   E2B    │
            │ Sandbox  │
            └──────────┘
```

### 3. Sandbox Isolation

Each agent task runs in an isolated E2B cloud sandbox:
- **Isolation**: Complete separation from host system
- **Resource Limits**: Configurable CPU, memory, and timeout limits
- **State Management**: Sandboxes are created per session and cleaned up after use

---

## Key Components

### Frontend (`/frontend`)
- React-based web interface
- Real-time updates via WebSocket
- File upload/download support
- Session history management

### Backend (`/backend`)
- FastAPI-based REST API
- WebSocket for real-time communication
- MongoDB for session persistence
- Redis for task queue management

### E2B Sandbox (`/backend/app/infrastructure/external/sandbox/`)
- **E2BSandbox**: Cloud-based execution environment
- **Terminal Tool**: Command execution
- **Browser Tool**: Headless Chrome automation
- **File Tool**: File operations (upload, download, read, write)

### Agent System (`/backend/app/domain/`)
- **Planner Agent**: Breaks down tasks into steps
- **Execution Agent**: Executes individual steps
- **Tool Registry**: Manages available tools and their configurations

---

## Sandbox System

### E2B Sandbox (Current Implementation)

The project now uses **E2B** as the sole sandbox provider. E2B provides cloud-based development environments that are:

- **Secure**: Isolated containers with no access to your infrastructure
- **Fast**: Spins up in seconds
- **Configurable**: Choose from various templates (base, python, nodejs)
- **Scalable**: Cloud-native architecture

#### Configuration

| Environment Variable | Description | Default |
|---------------------|-------------|---------|
| `E2B_API_KEY` | Your E2B API key (REQUIRED) | - |
| `E2B_TEMPLATE` | Sandbox template to use | `base` |
| `E2B_TIMEOUT` | Execution timeout (seconds) | 300 |

#### Available Templates

- `base`: Basic environment with common tools
- `python`: Python development environment
- `nodejs`: Node.js development environment
- `rust`: Rust development environment
- And more...

#### Getting E2B API Key

1. Go to [e2b.dev/dashboard](https://e2b.dev/dashboard)
2. Sign up for an account
3. Create a new API key
4. Add it to your `.env` file

---

## Technology Stack

### Frontend
- **React 18**: UI framework
- **TypeScript**: Type safety
- **Vite**: Build tool
- **TailwindCSS**: Styling
- **Socket.io-client**: Real-time communication

### Backend
- **Python 3.11+**: Runtime
- **FastAPI**: Web framework
- **Pydantic**: Data validation
- **MongoDB**: Database
- **Redis**: Cache and task queue
- **WebSocket**: Real-time communication

### AI/ML
- **OpenAI SDK**: OpenAI API integration
- **DeepSeek**: Alternative LLM provider
- **LangChain**: LLM orchestration (optional)

### Infrastructure
- **E2B**: Cloud sandbox execution
- **Docker**: Containerization (optional, for local deployment)

---

## Security Considerations

1. **Sandbox Isolation**: All code execution happens in isolated E2B containers
2. **API Key Security**: Never commit API keys to version control
3. **JWT Authentication**: Secure token-based authentication
4. **Input Validation**: All user inputs are validated and sanitized

---

## License

MIT License - See [LICENSE](LICENSE) for details.

---

## Support

- Documentation: [docs.ai-manus.com](https://docs.ai-manus.com)
- Demo: [app.ai-manus.com](https://app.ai-manus.com)
- GitHub: [github.com/simpleyyt/ai-manus](https://github.com/simpleyyt/ai-manus)
