# Prompt Refiner MCP

An independent FastMCP server for Prompt Refiner's one-prompt plus optional
controls contract. It refines prompt intent, structure, constraints, and
output instructions before a prompt reaches an LLM. It never calls an AI
provider, reads local files, or runs generated prompts.

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

Before connecting a client, inspect the server locally:

```bash
prompt-builder-mcp --list-tools
prompt-builder-mcp --schema
```
