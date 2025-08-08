# LangGraph Agent with MCP Web Search Tool

This project creates a LangGraph ReAct agent that uses a web search tool provided via the Model Context Protocol (MCP). The MCP server wraps DuckDuckGo search and is connected via stdio.

## Features
- MCP server exposing a `web_search` tool (DuckDuckGo-based)
- LangGraph agent that discovers and calls the MCP tool
- Local test script that doesn't require an LLM key

## Repo layout
- `mcp_web_search_server.py` — MCP server exposing `web_search` over stdio
- `agent.py` — LangGraph agent that loads MCP tools and answers questions
- `test_search.py` — Local test runner for `web_search` without MCP/LLM
- `requirements.txt` — Python dependencies

## Prerequisites
- Python 3.10+

## Setup
```bash
python -m venv /workspace/.venv
source /workspace/.venv/bin/activate
pip install -r /workspace/requirements.txt
```

## Quick test (no LLM key required)
```bash
python /workspace/test_search.py "LangGraph MCP integration"
```

## Run the LangGraph agent
Set your LLM key (OpenAI shown below) and run:
```bash
export OPENAI_API_KEY=sk-...   # or put this in a .env file
python /workspace/agent.py "Find top 3 recent articles about LangGraph MCP integration and summarize."
```

Environment variables:
- `OPENAI_API_KEY` — required for the agent
- `OPENAI_MODEL` — optional, defaults to `gpt-4o-mini`
- `MCP_WEB_SEARCH_SERVER_PATH` — optional, absolute path to the MCP server script (defaults to `/workspace/mcp_web_search_server.py`)

## Notes
- The MCP server uses stdio transport and is spawned as a subprocess by the agent.
- The `web_search` tool returns a list of results with `title`, `url`, and `snippet` fields.
