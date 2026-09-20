from prompt_builder_mcp.service import generate_prompt_variants, get_prompt_schema, validate_prompt_brief
from prompt_builder_mcp.server import main
import json


BRIEF = {"schema_version": "1.2", "type": "prompt_refinement", "user_prompt": "Write a launch plan", "task": "Write", "writing_form": "Email", "writing_intent": "Inform", "length": "Short", "audience": "Executive", "constraints": ["30 days"], "output": "Markdown", "tone": "Technical", "prompt_nature": 20}


def test_schema_describes_required_fields():
    assert "user_prompt" in get_prompt_schema()["required"]


def test_validation_reports_missing_fields():
    assert validate_prompt_brief({})["missing_fields"] == ["user_prompt"]


def test_variants_are_deterministic():
    result = generate_prompt_variants(BRIEF)
    assert result["validation"]["score"] == 100
    assert "User request: Write a launch plan" in result["variants"]["structured"]


def test_diagnostic_lists_public_tools(capsys):
    main(["--list-tools"])
    assert json.loads(capsys.readouterr().out)["tools"] == ["get_schema", "validate_brief", "build_prompt_variants"]


def test_image_controls_are_limited_to_image_prompts():
    assert validate_prompt_brief({"user_prompt": "A portrait", "task": "Image prompt", "aspect_ratio": "4:5"})["valid"]
    with __import__("pytest").raises(ValueError, match="not available"):
        validate_prompt_brief({"user_prompt": "A plan", "task": "Plan", "aspect_ratio": "4:5"})


def test_prompt_nature_uses_the_shared_zero_to_one_hundred_range():
    assert validate_prompt_brief({"user_prompt": "Be brief", "task": "Write", "prompt_nature": 0})["valid"]
    with __import__("pytest").raises(ValueError, match="0 to 100"):
        validate_prompt_brief({"user_prompt": "Be brief", "task": "Write", "prompt_nature": 101})
