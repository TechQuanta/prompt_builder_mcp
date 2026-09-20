# prompt_builder_mcp

An independent Python MCP server for deterministic prompt design. It does not
call an AI provider, read user files, or execute generated prompts.

## Tools

- `validate_prompt_brief`: validate and score a structured prompt brief.
- `generate_prompt_variants`: return focused, detailed, and structured prompts.
- `get_prompt_schema`: return the portable JSON schema clients should collect.

## Run

```bash
python -m pip install -e .
prompt-builder-mcp
```

Configure an MCP client with `prompt-builder-mcp` as its stdio command.
