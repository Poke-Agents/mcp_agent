from __future__ import annotations

import sys
from pprint import pprint

from mcp_web_search_server import web_search


def main() -> None:
    query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "LangGraph MCP"
    results = web_search(query, max_results=3)
    pprint(results)


if __name__ == "__main__":
    main()