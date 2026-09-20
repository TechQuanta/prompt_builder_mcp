"""Pure deterministic prompt-building operations."""

from __future__ import annotations

from typing import Any

REQUIRED_FIELDS = ("goal", "audience", "context", "output_format", "tone")
PROVIDERS = ("universal", "chatgpt", "claude", "gemini")


def get_prompt_schema() -> dict[str, Any]:
    return {
        "schema_version": "1.0",
        "type": "prompt_brief",
        "required": list(REQUIRED_FIELDS),
        "properties": {
            "goal": {"type": "string", "description": "The outcome the model should produce."},
            "audience": {"type": "string", "description": "Who will use the result."},
            "context": {"type": "string", "description": "Relevant facts and background."},
            "constraints": {"type": "array", "items": {"type": "string"}},
            "output_format": {"type": "string", "description": "Required response shape."},
            "tone": {"type": "string", "description": "Desired writing style."},
            "provider": {"type": "string", "enum": list(PROVIDERS), "default": "universal"},
        },
    }


def validate_prompt_brief(brief: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(brief, dict):
        raise ValueError("brief must be a JSON object.")
    provider = brief.get("provider", "universal")
    if provider not in PROVIDERS:
        raise ValueError(f"provider must be one of: {', '.join(PROVIDERS)}.")
    constraints = brief.get("constraints", [])
    if not isinstance(constraints, list) or not all(isinstance(item, str) for item in constraints):
        raise ValueError("constraints must be a list of strings.")
    missing = [field for field in REQUIRED_FIELDS if not isinstance(brief.get(field), str) or not brief[field].strip()]
    return {"valid": not missing, "score": round((len(REQUIRED_FIELDS) - len(missing)) / len(REQUIRED_FIELDS) * 100), "missing_fields": missing}


def generate_prompt_variants(brief: dict[str, Any]) -> dict[str, Any]:
    validation = validate_prompt_brief(brief)
    constraints = "; ".join(item.strip() for item in brief.get("constraints", []) if item.strip()) or "None provided"
    provider = brief.get("provider", "universal")
    provider_rule = {
        "chatgpt": "Follow the requested output format exactly.",
        "claude": "Think carefully and state material assumptions.",
        "gemini": "Use clear sections and make uncertainty explicit.",
        "universal": "Make assumptions explicit and do not invent facts.",
    }[provider]
    prefix = f"Goal: {brief.get('goal', '[define the goal]')}\nAudience: {brief.get('audience', '[define the audience]')}\nContext: {brief.get('context', '[add context]')}\nConstraints: {constraints}\nTone: {brief.get('tone', 'Clear and practical')}\n"
    variants = {
        "focused": f"{prefix}\nGive a direct answer with only essential reasoning. {provider_rule}\nReturn: {brief.get('output_format', 'Markdown')}",
        "detailed": f"{prefix}\nWork through the request carefully and explain important choices. {provider_rule}\nReturn: {brief.get('output_format', 'Markdown')}",
        "structured": f"{prefix}\nUse headings, a short summary, and a final checklist. {provider_rule}\nReturn: {brief.get('output_format', 'Markdown')}",
    }
    return {"validation": validation, "provider": provider, "variants": variants}
