from prompt_builder_mcp.service import generate_prompt_variants, get_prompt_schema, validate_prompt_brief


BRIEF = {"goal": "Write a launch plan", "audience": "Founders", "context": "B2B SaaS", "constraints": ["30 days"], "output_format": "Markdown", "tone": "Practical", "provider": "universal"}


def test_schema_describes_required_fields():
    assert "goal" in get_prompt_schema()["required"]


def test_validation_reports_missing_fields():
    assert validate_prompt_brief({"goal": "x"})["missing_fields"] == ["audience", "context", "output_format", "tone"]


def test_variants_are_deterministic():
    result = generate_prompt_variants(BRIEF)
    assert result["validation"]["score"] == 100
    assert "Goal: Write a launch plan" in result["variants"]["structured"]
