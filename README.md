# Prompt Builder MCP

An independent FastMCP server for Prompt Builder's one-prompt plus optional
controls contract. It never calls an AI provider, reads local files, or runs
generated prompts.

## Run

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install -e .
prompt-builder-mcp
```

MCP client configuration:

```json
{"mcpServers":{"prompt-builder":{"command":"prompt-builder-mcp"}}}
```

Tools: `get_schema`, `validate_brief`, and `build_prompt_variants`.
