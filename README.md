# Prompt Refiner MCP

Built openly by [TechQuanta Community](https://github.com/TechQuanta). Contributions are welcome through the repository's issues and pull requests.

An independent FastMCP server for Prompt Refiner's schema v1.3 one-prompt plus optional
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

## Horizon Deploy

Use the repository form with these values:

| Field | Value |
| --- | --- |
| Server name | `prompt-builder` |
| Entrypoint | `server.py` |
| Requirements | `requirements.txt` |
| Transport | Streamable HTTP |

The root `server.py` adds the `src/` package path, binds to `HOST` (default
`0.0.0.0`) and `PORT` (default `8000`), and serves the MCP endpoint at
`/mcp`. It is intended for hosted deployment and does not replace the local
stdio entry point.

For local HTTP testing:

```powershell
python server.py
```

For a local stdio client:

```powershell
prompt-builder-mcp
```
