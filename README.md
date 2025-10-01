# MCP LangChain Multi-Server Demo

A demonstration project showcasing the integration of multiple Model Context Protocol (MCP) servers with LangChain and LangGraph to create an intelligent agent capable of performing math operations and weather queries.

## Overview

This project demonstrates how to:
- Set up multiple MCP servers (Math and Weather)
- Connect them using LangChain's MCP adapters
- Create a ReAct agent with LangGraph that can intelligently choose and use the appropriate tools
- Execute multi-step reasoning tasks across different domains

## Project Structure

```
.
├── client.py          # Main agent client that orchestrates multiple MCP servers
├── mathserver.py      # MCP server providing mathematical operations
├── weather.py         # MCP server providing weather information
├── main.py            # Legacy/unused file (can be removed)
├── .env               # Environment variables (OpenAI API key)
└── README.md          # This file
```

## Features

### Math Server
- **Add**: Add two numbers
- **Multiply**: Multiply two numbers

### Weather Server
- **Get Weather**: Retrieve weather information for any location

### Intelligent Agent
- Uses OpenAI's GPT-4o-mini model
- Automatically selects appropriate tools based on user queries
- Handles multi-step reasoning (e.g., "add 3 and 5, then multiply by 12")

## Prerequisites

- Python 3.8 or higher
- OpenAI API key
- pip or poetry for package management

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Install required dependencies:
```bash
pip install langchain-mcp-adapters langgraph langchain-openai python-dotenv mcp
```

3. Create a `.env` file in the project root:
```bash
OPENAI_API_KEY=your_openai_api_key_here
```

## Usage

Run the client to see the agent in action:

```bash
python client.py
```

### Example Output

The script demonstrates two types of queries:

1. **Math Query**: "what's (3 + 5) x 12?"
   - The agent will use the math server's `add` and `multiply` tools
   - Expected result: 96

2. **Weather Query**: "what is the weather in California?"
   - The agent will use the weather server's `get_weather` tool
   - Returns a simulated weather response

## How It Works

### 1. MCP Servers

The project uses FastMCP to create lightweight MCP servers:

- **mathserver.py**: Exposes `add` and `multiply` functions as tools
- **weather.py**: Exposes `get_weather` function as a tool

Each server runs independently and communicates via standard input/output (stdio).

### 2. Client Configuration

The `client.py` file:
- Initializes `MultiServerMCPClient` with configuration for both servers
- Retrieves all available tools from both servers
- Creates a ReAct agent using LangGraph
- Sends queries to the agent, which intelligently selects and uses the appropriate tools

### 3. Agent Workflow

```
User Query → Agent (GPT-4o-mini) → Tool Selection → MCP Server → Response → Agent → Final Answer
```

## Architecture

```
┌─────────────────────────────────────────┐
│           client.py                      │
│  ┌───────────────────────────────────┐  │
│  │  MultiServerMCPClient             │  │
│  │  ┌─────────────┐  ┌─────────────┐ │  │
│  │  │   Math      │  │   Weather   │ │  │
│  │  │   Server    │  │   Server    │ │  │
│  │  └─────────────┘  └─────────────┘ │  │
│  └───────────────────────────────────┘  │
│                                          │
│  ┌───────────────────────────────────┐  │
│  │  LangGraph ReAct Agent            │  │
│  │  (GPT-4o-mini)                    │  │
│  └───────────────────────────────────┘  │
└─────────────────────────────────────────┘
```

## Extending the Project

### Adding New Tools to Existing Servers

Edit `mathserver.py` or `weather.py`:

```python
@mcp.tool()
def subtract(a: int, b: int) -> int:
    """Subtract b from a"""
    return a - b
```

### Adding a New MCP Server

1. Create a new server file (e.g., `dateserver.py`):
```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Date")

@mcp.tool()
def get_current_date() -> str:
    """Get the current date"""
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d")

if __name__ == "__main__":
    mcp.run(transport="stdio")
```

2. Add it to the client configuration in `client.py`:
```python
client = MultiServerMCPClient({
    "Math": {...},
    "Weather": {...},
    "Date": {
        "command": "python",
        "args": ["dateserver.py"],
        "transport": "stdio",
    }
})
```

## Troubleshooting

### Import Errors
Ensure all dependencies are installed:
```bash
pip install --upgrade langchain-mcp-adapters langgraph langchain-openai python-dotenv mcp
```

### OpenAI API Key Issues
- Verify your `.env` file contains a valid `OPENAI_API_KEY`
- Check that the key has sufficient credits

### Server Communication Issues
- Ensure server files have correct paths in the client configuration
- Check that Python is in your system PATH
- Verify server files are executable

## Dependencies

- `langchain-mcp-adapters`: Adapter for integrating MCP servers with LangChain
- `langgraph`: Framework for building stateful agents
- `langchain-openai`: OpenAI integration for LangChain
- `python-dotenv`: Environment variable management
- `mcp`: Model Context Protocol library

## License

[Your License Here]

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Resources

- [MCP Documentation](https://modelcontextprotocol.io/)
- [LangChain Documentation](https://python.langchain.com/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [FastMCP](https://github.com/jlowin/fastmcp)

## Author

[Your Name/Organization]

## Acknowledgments

- Anthropic for the Model Context Protocol
- LangChain team for the excellent tooling
- OpenAI for the language models
