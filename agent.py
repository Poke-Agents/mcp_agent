from __future__ import annotations

import os
import sys
import asyncio
from typing import Any, Dict

from dotenv import load_dotenv
from langgraph.prebuilt import create_react_agent
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import ChatOpenAI


load_dotenv()


async def main() -> None:
    # LLM configuration
    openai_api_key = os.getenv("OPENAI_API_KEY")
    model_name = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    if not openai_api_key:
        raise RuntimeError(
            "OPENAI_API_KEY is not set. Set it in environment or .env to run the agent.\n"
            "You can still test the MCP tool with: python /workspace/test_search.py 'your query'"
        )

    model = ChatOpenAI(model=model_name, api_key=openai_api_key)

    # Resolve path to MCP server
    server_path = os.path.abspath(
        os.getenv("MCP_WEB_SEARCH_SERVER_PATH", "/workspace/mcp_web_search_server.py")
    )
    if not os.path.exists(server_path):
        raise FileNotFoundError(f"MCP server not found at {server_path}")

    # Initialize MCP client for the web search server (stdio transport)
    client = MultiServerMCPClient(
        {
            "web_search": {
                "command": sys.executable,
                "args": [server_path],
                "transport": "stdio",
            }
        }
    )

    tools = await client.get_tools()

    # Create a simple ReAct agent bound to MCP tools
    agent = create_react_agent(model, tools)

    user_query = (
        " ".join(sys.argv[1:])
        if len(sys.argv) > 1
        else "Find top 3 recent articles about LangGraph MCP integration and summarize."
    )

    result: Dict[str, Any] = await agent.ainvoke(
        {"messages": [{"role": "user", "content": user_query}]}
    )
    last_message = result["messages"][-1]
    print(last_message.content)

    await client.close()


if __name__ == "__main__":
    asyncio.run(main())