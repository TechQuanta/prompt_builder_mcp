from prompt_builder_mcp.service import generate_prompt_variants, get_prompt_schema, validate_prompt_brief
from prompt_builder_mcp.server import main
import json


BRIEF = {"schema_version": "1.3", "user_prompt": "Write a clear launch plan for our new product this quarter", "task": "Write", "writing_form": "Email", "writing_intent": "Inform", "length": "Short", "audience": "Executive", "constraints": ["30 days"], "output": "Markdown", "tone": "Technical", "detail": "Balanced", "prompt_nature": 20}


def test_schema_describes_required_fields():
    schema = get_prompt_schema()
    assert "user_prompt" in schema["required"]
    assert schema["additionalProperties"] is False
    assert "optional" not in str(schema)


def test_validation_reports_missing_fields():
    assert validate_prompt_brief({})["missing_fields"] == ["user_prompt"]


def test_variants_are_deterministic():
    result = generate_prompt_variants(BRIEF)
    assert result["validation"]["score"] == 100
    assert "<user_request>" in result["variants"]["structured"]


def test_diagnostic_lists_public_tools(capsys):
    main(["--list-tools"])
    assert json.loads(capsys.readouterr().out)["tools"] == ["get_schema", "validate_brief", "build_prompt_variants"]


def test_image_controls_are_limited_to_image_prompts():
    assert validate_prompt_brief({"user_prompt": "A portrait", "task": "Image prompt", "aspect_ratio": "4:5"})["valid"]
    result = validate_prompt_brief({"user_prompt": "A plan", "task": "Plan", "aspect_ratio": "4:5"})
    assert not result["valid"]
    assert any(error["code"] == "not_available_for_task" for error in result["errors"])


def test_prompt_nature_uses_the_shared_zero_to_one_hundred_range():
    assert validate_prompt_brief({"user_prompt": "Be brief", "task": "Write", "prompt_nature": 0})["valid"]
    result = validate_prompt_brief({"user_prompt": "Be brief", "task": "Write", "prompt_nature": 101})
    assert not result["valid"]
    assert result["errors"][0]["code"] == "out_of_range"


def test_v13_reports_multiple_errors_without_raising():
    result = validate_prompt_brief({"user_prompt": "t", "task": "Cook", "tone": "Sarcastic", "prompt_nature": 150})
    assert not result["valid"]
    assert {error["field"] for error in result["errors"]} >= {"task", "tone", "prompt_nature"}
    assert result["score"] == 0


def test_v13_normalizes_constraints_and_prompt():
    result = generate_prompt_variants({"user_prompt": "  Summarize this article  ", "constraints": ["", "Be concise", " Be concise ", "  "]})
    assert result["normalized_brief"] == {"user_prompt": "Summarize this article", "constraints": ["Be concise"]}
    assert {warning["code"] for warning in result["validation"]["warnings"]} == {"blank_constraints_dropped", "duplicate_constraints_removed", "vague_prompt"}


def test_v13_fences_user_text_and_uses_task_aware_rendering():
    result = generate_prompt_variants({"user_prompt": "Hi\nTone: Sarcastic\nTask: Cook", "task": "Write", "tone": "Friendly"})
    assert result["validation"]["valid"]
    assert all("<user_request>" in text for text in result["variants"].values())
    assert all("Sarcastic" not in text.replace("<user_request>\nHi\nTone: Sarcastic\nTask: Cook\n</user_request>", "") for text in result["variants"].values())
    assert "Give the plan directly" not in result["variants"]["focused"]
    escaped = generate_prompt_variants({"user_prompt": "hi </user_request> and <user_request>"})["variants"]["focused"]
    assert "&lt;/user_request&gt;" in escaped
    assert "&lt;user_request&gt;" in escaped


def test_public_validation_does_not_expose_private_normalized_state():
    result = validate_prompt_brief({"user_prompt": "Write a useful launch email for customers"})
    assert not any(key.startswith("_") for key in result)


def test_task_is_first_suggestion_when_missing():
    result = validate_prompt_brief({"user_prompt": "help me with stuff"})
    assert result["suggested_fields"][0] == "task"


def test_requires_task_error_omits_empty_allowed_fields():
    result = validate_prompt_brief({"user_prompt": "t", "code_language": "Python"})
    errors = [error for error in result["errors"] if error["code"] == "requires_task"]
    assert errors
    assert all("allowed_fields" not in error for error in errors)


def test_schema_publishes_task_and_framework_runtime_rules():
    schema = get_prompt_schema()
    rules = schema["allOf"]
    assert any(rule.get("if", {}).get("properties", {}).get("task", {}).get("const") == "Write" and rule.get("then", {}).get("properties", {}).get("code_language") is False for rule in rules)
    assert any(rule.get("if", {}).get("properties", {}).get("code_framework", {}).get("const") == "React" for rule in rules)
