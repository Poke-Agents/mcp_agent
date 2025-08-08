from __future__ import annotations

from typing import List, Dict, Optional

from mcp.server.fastmcp import FastMCP
from duckduckgo_search import DDGS

mcp = FastMCP("WebSearch")


@mcp.tool()
def web_search(
    query: str,
    max_results: int = 5,
    region: str = "us-en",
    safesearch: str = "moderate",
    time: Optional[str] = None,
) -> List[Dict[str, str]]:
    """Search the web using DuckDuckGo and return concise results.

    Args:
        query: Search query.
        max_results: Maximum number of results to return.
        region: Region code (e.g., 'us-en').
        safesearch: One of 'off', 'moderate', 'strict'.
        time: Optional time filter (e.g., 'd', 'w', 'm', 'y').

    Returns:
        A list of dicts with keys: title, url, snippet, source.
    """
    results: List[Dict[str, str]] = []
    with DDGS() as ddgs:
        for item in ddgs.text(
            query,
            region=region,
            safesearch=safesearch,
            timelimit=time,
            max_results=max_results,
        ):
            results.append(
                {
                    "title": item.get("title", ""),
                    "url": item.get("href", ""),
                    "snippet": item.get("body", ""),
                    "source": "duckduckgo",
                }
            )
    return results


if __name__ == "__main__":
    # Run as an MCP stdio server
    mcp.run(transport="stdio")