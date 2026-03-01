# 🤖 AI Manus Open Source General AI Agent

Project URL: <https://github.com/Simpleyyt/ai-manus>

Join our community: [Discord](https://discord.gg/manus)

---

AI Manus is a general-purpose AI Agent system that can be fully privately deployed and supports running various tools and operations in a sandbox environment.

The goal of AI Manus project is to become a fully privately deployable enterprise-level Manus application. Vertical Manus applications have many repetitive engineering tasks, and this project hopes to unify this part, allowing everyone to build vertical Manus applications like building blocks.

Each service and tool in AI Manus includes a Built-in version that can be fully privately deployed. Later, through A2A and MCP protocols, both Built-in Agents and Tools can be replaced. The underlying infrastructure can also be replaced by providing diverse provider configurations or simple development adaptations. AI Manus supports distributed multi-instance deployment from the architectural design, facilitating horizontal scaling to meet enterprise-level deployment requirements.

---

## Basic Features

[](https://github.com/user-attachments/assets/37060a09-c647-4bcb-920c-959f7fa73ebe ':include :type=video controls width="100%"')

## Core Features

 * **Deployment:** Only requires an LLM service and E2B API key for deployment
 * **Tools:** Supports Terminal, Browser, File, Web Search, message tools, with real-time viewing
 * **Sandbox:** Each Task runs in an isolated E2B cloud sandbox
 * **Task Sessions:** Manages session history through MongoDB/Redis, supports background tasks
 * **Conversations:** Supports stopping and interruption, supports file upload and download
 * **Multi-language:** Supports English and Chinese
 * **Authentication:** User login and authentication

---

## Quick Links

- [🚀 Quick Start](quick_start.md)
- [📋 Configuration](configuration.md)
- [⚙️ System Architecture](architecture.md)
- [🔧 MCP Configuration](mcp.md)
