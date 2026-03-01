# ⚙️ System Architecture

## Overall Design

![Image](https://github.com/user-attachments/assets/69775011-1eb7-452f-adaf-cd6603a4dde5 ':size=600')

**When a user initiates a conversation:**

1. Web sends a create Agent request to Server, Server creates an E2B Sandbox and returns session ID.
2. Sandbox is an isolated E2B cloud environment with code execution, browser automation, and file/shell tools.
3. Web sends user messages to the session ID, Server receives user messages and forwards them to PlanAct Agent for processing.
4. PlanAct Agent calls relevant tools to complete tasks during processing.
5. All events generated during Agent processing are sent back to Web via SSE.

**When users use tools:**

- Terminal: Commands execute in the E2B sandbox environment
- Browser: Headless browser automation via Playwright in E2B
- File operations: Files are managed within the E2B sandbox
- Other tools: Similar principles apply

## E2B Sandbox

AI Manus uses E2B cloud sandboxes for secure code execution:

- **Isolation**: Each sandbox runs in an isolated container
- **No Docker required**: Cloud-based execution
- **Fast startup**: Sandboxes spin up in seconds
- **Scalable**: Cloud-native architecture
