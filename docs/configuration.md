# 📋 Configuration Guide

## Configuration Items

### Model Provider Configuration

| Configuration | Default Value | Required | Description |
|---------------|---------------|----------|-------------|
| `API_KEY` | - | Yes | API key for the LLM model |
| `API_BASE` | `https://api.deepseek.com/v1` | Yes | Base API address for model service |

### Model Configuration

| Configuration | Default Value | Required | Description |
|---------------|---------------|----------|-------------|
| `MODEL_NAME` | `deepseek-chat` | No | Name of the model to use |
| `TEMPERATURE` | `0.7` | No | Randomness level, range 0-1 |
| `MAX_TOKENS` | `2000` | No | Maximum tokens in response |

### E2B Sandbox Configuration

| Configuration | Default Value | Required | Description |
|---------------|---------------|----------|-------------|
| `E2B_API_KEY` | - | Yes | E2B API key from https://e2b.dev/dashboard |
| `E2B_TEMPLATE` | `base` | No | E2B sandbox template (base, python, nodejs, rust) |
| `E2B_TIMEOUT` | `300` | No | Execution timeout in seconds |

### MongoDB Configuration

| Configuration | Default Value | Required | Description |
|---------------|---------------|----------|-------------|
| `MONGODB_URI` | `MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net` | No | MongoDB connection string |
| `MONGODB_DATABASE` | `manus` | No | Database name |
| `MONGODB_USERNAME` | - | No | MongoDB username |
| `MONGODB_PASSWORD` | - | No | MongoDB password |

### Redis Configuration

| Configuration | Default Value | Required | Description |
|---------------|---------------|----------|-------------|
| `REDIS_HOST` | `redis` | No | Redis server address |
| `REDIS_PORT` | `6379` | No | Redis server port |
| `REDIS_DB` | `0` | No | Redis database number |
| `REDIS_PASSWORD` | - | No | Redis password |

### Search Engine Configuration

| Configuration | Default Value | Required | Description |
|---------------|---------------|----------|-------------|
| `SEARCH_PROVIDER` | `bing` | No | Search provider (`baidu`, `google`, `bing`) |

#### Google Search Configuration

Used only when `SEARCH_PROVIDER=google`:

| Configuration | Default Value | Required | Description |
|---------------|---------------|----------|-------------|
| `GOOGLE_SEARCH_API_KEY` | - | Yes | Google Search API key |
| `GOOGLE_SEARCH_ENGINE_ID` | - | Yes | Google Custom Search Engine ID |

### Authentication Configuration

| Configuration | Default Value | Required | Description |
|---------------|---------------|----------|-------------|
| `AUTH_PROVIDER` | `password` | No | Auth provider (`password`, `none`, `local`) |

#### Password Authentication Configuration

Used only when `AUTH_PROVIDER=password`:

| Configuration | Default Value | Required | Description |
|---------------|---------------|----------|-------------|
| `PASSWORD_SALT` | - | No | Password encryption salt |
| `PASSWORD_HASH_ROUNDS` | `10` | No | Password hash rounds |

#### Local Authentication Configuration

Used only when `AUTH_PROVIDER=local`:

| Configuration | Default Value | Required | Description |
|---------------|---------------|----------|-------------|
| `LOCAL_AUTH_EMAIL` | `admin@example.com` | No | Local admin email |
| `LOCAL_AUTH_PASSWORD` | `admin` | No | Local admin password |

### JWT Configuration

| Configuration | Default Value | Required | Description |
|---------------|---------------|----------|-------------|
| `JWT_SECRET_KEY` | `your-secret-key-here` | Yes | JWT signing key |
| `JWT_ALGORITHM` | `HS256` | No | JWT algorithm |
| `JWT_ACCESS_TOKEN_EXPIRE_MINUTES` | `30` | No | Access token expiration |
| `JWT_REFRESH_TOKEN_EXPIRE_DAYS` | `7` | No | Refresh token expiration |

### Email Configuration

Used only when `AUTH_PROVIDER=password`:

| Configuration | Default Value | Required | Description |
|---------------|---------------|----------|-------------|
| `EMAIL_HOST` | - | No | SMTP server address |
| `EMAIL_PORT` | `587` | No | SMTP server port |
| `EMAIL_USERNAME` | - | No | Email username |
| `EMAIL_PASSWORD` | - | No | Email password |
| `EMAIL_FROM` | - | No | Sender email address |

### MCP Configuration

| Configuration | Default Value | Required | Description |
|---------------|---------------|----------|-------------|
| `MCP_CONFIG_PATH` | `/etc/mcp.json` | No | MCP configuration file path |

### Log Configuration

| Configuration | Default Value | Required | Description |
|---------------|---------------|----------|-------------|
| `LOG_LEVEL` | `INFO` | No | Log level (`DEBUG`, `INFO`, `WARNING`, `ERROR`) |
