"""FastMCP stdio server for Prompt Refiner."""

from __future__ import annotations

import argparse
import json
import os
from typing import Any

from fastmcp import FastMCP
from .service import generate_prompt_variants, get_prompt_schema, validate_prompt_brief

mcp = FastMCP("prompt-refiner")
TOOL_NAMES = ("get_schema", "validate_brief", "build_prompt_variants")


@mcp.tool()
def get_schema() -> dict[str, Any]:
    """Return the JSON schema for a deterministic prompt brief."""
    return get_prompt_schema()


@mcp.tool()
def validate_brief(brief: dict[str, Any]) -> dict[str, Any]:
    """Validate a prompt brief and report its completeness score."""
    return validate_prompt_brief(brief)


@mcp.tool()
def build_prompt_variants(brief: dict[str, Any]) -> dict[str, Any]:
    """Build focused, detailed, and structured prompt variants without calling an LLM."""
    return generate_prompt_variants(brief)


def main(argv: list[str] | None = None) -> None:
    """Run the MCP server over stdio or print local diagnostics."""
    parser = argparse.ArgumentParser(description="Run the Prompt Refiner MCP server.")
    parser.add_argument("--list-tools", action="store_true", help="Print tool names and exit.")
    parser.add_argument("--schema", action="store_true", help="Print the prompt brief schema and exit.")
    parser.add_argument(
        "--transport", choices=("stdio", "http", "streamable-http"), default="stdio",
        help="Transport to run (default: stdio).",
    )
    parser.add_argument("--host", default=os.environ.get("HOST", "127.0.0.1"), help="HTTP host.")
    parser.add_argument("--port", type=int, default=int(os.environ.get("PORT", "8000")), help="HTTP port.")
    args = parser.parse_args(argv)
    if args.list_tools:
        print(json.dumps({"server": "prompt-refiner", "tools": list(TOOL_NAMES)}, indent=2))
        return
    if args.schema:
        print(json.dumps(get_prompt_schema(), indent=2))
        return
    if not 1 <= args.port <= 65535:
        parser.error("--port must be between 1 and 65535.")
    transport = "http" if args.transport == "streamable-http" else args.transport
    run_options: dict[str, Any] = {"transport": transport}
    if transport != "stdio":
        run_options.update({"host": args.host, "port": args.port})
        if transport == "http":
            run_options["path"] = "/mcp"
    mcp.run(**run_options)


if __name__ == "__main__":
    main()
