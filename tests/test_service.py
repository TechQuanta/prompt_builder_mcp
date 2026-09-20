from prompt_builder_mcp.service import generate_prompt_variants, get_prompt_schema, validate_prompt_brief


BRIEF = {"user_prompt": "Write a launch plan", "audience": "Executive", "constraints": ["30 days"], "output": "Markdown", "tone": "Technical"}


def test_schema_describes_required_fields():
    assert "user_prompt" in get_prompt_schema()["required"]


def test_validation_reports_missing_fields():
    assert validate_prompt_brief({})["missing_fields"] == ["user_prompt"]


def test_variants_are_deterministic():
    result = generate_prompt_variants(BRIEF)
    assert result["validation"]["score"] == 100
    assert "User request: Write a launch plan" in result["variants"]["structured"]
