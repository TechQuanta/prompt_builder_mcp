"""Deterministic Prompt Refiner schema and variant operations."""

from __future__ import annotations

from typing import Any

SHARED_OPTIONS = {
    "task": ("Write", "Research", "Plan", "Code", "Image prompt"),
    "tone": ("Clear", "Concise", "Creative", "Technical", "Friendly", "Persuasive", "Playful", "Professional"),
    "output": ("Markdown", "JSON", "Table", "Checklist", "Timeline", "Step-by-step"),
    "detail": ("Brief", "Balanced", "In-depth"),
}
TYPE_OPTIONS = {
    "Write": {
        "writing_form": ("Email", "Post", "Article", "Script", "Ad copy"),
        "audience": ("General", "Beginner", "Professional", "Executive"),
        "writing_intent": ("Inform", "Engage", "Persuade", "Sell", "Inspire"),
        "length": ("Short", "Medium", "Long", "Long-form"),
    },
    "Research": {
        "research_mode": ("Compare", "Explain", "Evaluate", "Summarize"),
        "source_policy": ("Cite sources", "Primary sources", "No web sources"),
        "depth": ("Quick", "Balanced", "Thorough"),
        "research_scope": ("Overview", "Practical", "Academic", "Market"),
    },
    "Plan": {
        "planning_horizon": ("Today", "This week", "30 days", "Quarter"),
        "planning_approach": ("Step-by-step", "Milestones", "Prioritized", "Risk-first"),
        "audience": ("Individual", "Team", "Leadership", "Customer"),
        "priority": ("Speed", "Impact", "Cost", "Quality"),
    },
    "Code": {
        "code_language": ("Python", "TypeScript", "JavaScript", "SQL", "Java"),
        "code_framework": ("React", "Next.js", "FastAPI", "Django", "Node.js"),
        "code_intent": ("Write", "Debug", "Review", "Refactor", "Explain"),
        "code_tests": ("Include tests", "Test plan", "No tests"),
    },
    "Image prompt": {
        "visual_style": ("Photorealistic", "Editorial", "Illustration", "3D render", "Minimal"),
        "aspect_ratio": ("1:1", "4:5", "16:9", "9:16"),
        "lighting": ("Natural", "Studio", "Cinematic", "Soft"),
        "image_composition": ("Close-up", "Wide shot", "Flat lay", "Rule of thirds"),
        "color_mood": ("Neutral", "Warm", "Cool", "High contrast"),
    },
}

ALL_OPTIONS = {**SHARED_OPTIONS}
for group in TYPE_OPTIONS.values():
    for key, values in group.items():
        ALL_OPTIONS[key] = tuple(dict.fromkeys((*ALL_OPTIONS.get(key, ()), *values)))


def get_prompt_schema() -> dict[str, Any]:
    """Return the contract used by the browser and MCP tools."""
    properties = {
        "user_prompt": {"type": "string", "description": "The only free-text input."},
        "prompt_nature": {"type": "number", "minimum": 0, "maximum": 100, "optional": True},
        "constraints": {"type": "array", "items": {"type": "string"}, "optional": True},
        **{key: {"type": "string", "enum": list(values), "optional": True} for key, values in ALL_OPTIONS.items()},
    }
    return {
        "schema_version": "1.2",
        "type": "prompt_refinement",
        "required": ["user_prompt"],
        "properties": properties,
        "shared_controls": list(SHARED_OPTIONS),
        "control_groups": TYPE_OPTIONS,
    }


def validate_prompt_brief(brief: dict[str, Any]) -> dict[str, Any]:
    """Validate a portable Prompt Refiner brief without calling an LLM."""
    if not isinstance(brief, dict):
        raise ValueError("brief must be a JSON object.")

    missing = [] if isinstance(brief.get("user_prompt"), str) and brief["user_prompt"].strip() else ["user_prompt"]
    task = brief.get("task")
    for key, value in brief.items():
        if key in ALL_OPTIONS and value not in ALL_OPTIONS[key]:
            raise ValueError(f"{key} has an unsupported value: {value!r}.")
    if "prompt_nature" in brief and (not isinstance(brief["prompt_nature"], (int, float)) or not 0 <= brief["prompt_nature"] <= 100):
        raise ValueError("prompt_nature must be a number from 0 to 100.")
    if "constraints" in brief and (not isinstance(brief["constraints"], list) or not all(isinstance(item, str) for item in brief["constraints"])):
        raise ValueError("constraints must be a list of strings.")

    specific_keys = set().union(*(set(group) for group in TYPE_OPTIONS.values()))
    invalid = specific_keys.intersection(brief) - set(TYPE_OPTIONS.get(task, {}))
    if invalid:
        raise ValueError(f"{', '.join(sorted(invalid))} is not available for task {task!r}.")
    return {"valid": not missing, "score": 100 if not missing else 0, "missing_fields": missing}


def generate_prompt_variants(brief: dict[str, Any]) -> dict[str, Any]:
    """Generate deterministic prompt variants from a validated brief."""
    validation = validate_prompt_brief(brief)
    metadata = {"user_prompt", "schema_version", "type", "constraints"}
    selected = {key: value for key, value in brief.items() if key not in metadata and value not in (None, "None", [], 50)}
    lines = [f"User request: {brief.get('user_prompt', '[Enter your prompt]')}"]
    lines.extend(f"{key.replace('_', ' ').title()}: {value}" for key, value in selected.items())
    if brief.get("constraints"):
        lines.append(f"Constraints: {'; '.join(brief['constraints'])}")
    base = "\n".join(lines)
    return {
        "validation": validation,
        "normalized_brief": {"user_prompt": brief.get("user_prompt"), **selected},
        "variants": {
            "focused": f"{base}\n\nGive a direct, useful answer.",
            "detailed": f"{base}\n\nExplain important decisions and cover relevant edge cases.",
            "structured": f"{base}\n\nUse clear headings, a short summary, and a final checklist.",
        },
    }
