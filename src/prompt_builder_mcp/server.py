"""FastMCP stdio server for Prompt Builder."""

from __future__ import annotations

import argparse
import json
from typing import Any

from fastmcp import FastMCP
from .service import generate_prompt_variants, get_prompt_schema, validate_prompt_brief

mcp = FastMCP("prompt-builder")
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
    parser = argparse.ArgumentParser(description="Run the Prompt Builder MCP server.")
    parser.add_argument("--list-tools", action="store_true", help="Print tool names and exit.")
    parser.add_argument("--schema", action="store_true", help="Print the prompt brief schema and exit.")
    args = parser.parse_args(argv)
    if args.list_tools:
        print(json.dumps({"server": "prompt-builder", "tools": list(TOOL_NAMES)}, indent=2))
        return
    if args.schema:
        print(json.dumps(get_prompt_schema(), indent=2))
        return
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
