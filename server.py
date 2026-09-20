"""Horizon Deploy entry point for the Prompt Refiner MCP server."""

from __future__ import annotations

import os
import sys
from pathlib import Path

SOURCE_DIRECTORY = (Path(__file__).resolve().parent / "src").resolve()
if str(SOURCE_DIRECTORY) not in sys.path:
    sys.path.insert(0, str(SOURCE_DIRECTORY))

from prompt_builder_mcp.server import mcp


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    if not 1 <= port <= 65535:
        raise SystemExit("PORT must be between 1 and 65535")
    mcp.run(
        transport="http",
        host=os.environ.get("HOST", "0.0.0.0"),
        port=port,
        path="/mcp",
    )
