# MCP-CB Project Instructions

## Project Overview
Python 3.12 Telegram chatbot that integrates ChatGPT/DeepSeek API with MCP (Model Context Protocol) fetch server for web page parsing and summarization.

## Architecture
- **Bot Framework**: `telebot` library for Telegram integration
- **AI Backend**: OpenAI-compatible API (DeepSeek) for intelligent responses
- **MCP Integration**: Docker-based MCP fetch server via official Python SDK
  - Parses web pages and converts to Markdown format
  - Runs via Docker: `docker run -i --rm mcp/fetch`
  - Uses `mcp` Python library for async communication

## Development Setup
- **Python Version**: 3.12 (pinned in `.python-version`)
- **Dependency Management**: `pyproject.toml` with key dependencies:
  - `pytelegrambotapi` - Telegram bot API
  - `openai` - OpenAI-compatible API client
  - `mcp` - Official MCP Python SDK for server communication
- **Docker**: Required for MCP fetch server
- **Virtual Environment**: `.venv/` directory (gitignored)

## Key Workflows
1. **Environment Setup**: 
   - Ensure Python 3.12 and Docker installed
   - Create/activate `.venv`
   - Install dependencies: `pip install -e .` (from pyproject.toml)
   - Pull Docker image: `docker pull mcp/fetch`
2. **Running**: Execute `python main.py`
3. **Testing**: Run inline tests or verify imports with `python -c "import bot, mcp_client"`

## Implementation Notes
- **URL Detection**: Bot uses regex to extract URLs from messages
- **MCP Fetch**: Async communication with Docker container via stdio
- **Content Limiting**: Page content truncated to 8000 chars before sending to ChatGPT
- **Error Handling**: Simple logging for MCP and API failures
- **Polling Mode**: Low traffic expected, simple polling sufficient

## Key Files
- `main.py` - Entry point with config loading and validation
- `bot.py` - Telegram bot logic, URL detection, ChatGPT integration
- `mcp_client.py` - MCP client using official SDK, handles fetch operations
- `pyproject.toml` - Project configuration and dependencies
- `uv.lock` - Lock file for exact dependency reproduction
- `config.json` - Configuration (not in git, see `config.json.example`)
- `.python-version` - Python version specification (3.12)

## Coding Conventions
- Follow Python 3.12+ idioms and type hints
- Use async/await for MCP operations (`asyncio.run()` for sync context)
- Entry point: `if __name__ == "__main__":` block in `main.py`
- Regex for URL extraction: `r'https?://[^\s<>"{}|\\^`\[\]]+'`

## MCP Server Configuration
```json
{
  "mcpServers": {
    "fetch": {
      "command": "docker",
      "args": ["run", "-i", "--rm", "mcp/fetch"]
    }
  }
}
```

## Next Steps for AI Agents
When implementing features:
1. Ensure Docker is running and `mcp/fetch` image is pulled
2. Use official `mcp` library for MCP communication (not manual JSON-RPC)
3. Handle async operations properly with `asyncio.run()`
4. Test with `python -c "import bot, mcp_client"` before full bot integration
5. Use `pip install -e .` for development installation from pyproject.toml
