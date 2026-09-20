"""FastMCP stdio server for Prompt Builder."""

from __future__ import annotations

from typing import Any

from fastmcp import FastMCP
from .service import generate_prompt_variants, get_prompt_schema, validate_prompt_brief

mcp = FastMCP("prompt-builder")


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


def main() -> None:
    """Run the MCP server over stdio."""
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
