"""Tests for render_spec() output."""

from pathlib import Path

from codework.plan import (
    DEFAULT_STORY,
    Environment,
    ExercisePlan,
    Infrastructure,
    ProjectStage,
)
from codework.spec import render_spec


def _make_plan(**overrides) -> ExercisePlan:
    defaults = dict(
        root=Path("/tmp/test"),
        environment=Environment.cli_app,
        infrastructure=Infrastructure.local,
        project_stage=ProjectStage.greenfield,
        tasks=3,
        languages=["python"],
        technologies=[],
        algorithms=["two_sum"],
        prompt="",
        story=DEFAULT_STORY,
    )
    defaults.update(overrides)
    return ExercisePlan(**defaults)  # type: ignore[arg-type]


def test_render_spec_contains_front_matter():
    spec = render_spec(_make_plan())
    assert spec.startswith("---\n")
    assert "environment: cli_app" in spec
    assert "infrastructure: local" in spec
    assert "project_stage: greenfield" in spec


def test_render_spec_contains_definitions():
    spec = render_spec(_make_plan())
    assert "## Definitions" in spec
    assert "CLI Application" in spec
    assert "Local" in spec
    assert "Greenfield" in spec


def test_render_spec_contains_algorithm_info():
    spec = render_spec(_make_plan(algorithms=["two_sum", "coin_change"]))
    assert "Two Sum" in spec
    assert "Coin Change" in spec
    assert "Arrays & Hashing" in spec
    assert "Dynamic Programming" in spec


def test_render_spec_uses_pytest_for_python():
    spec = render_spec(_make_plan(languages=["python"]))
    assert "pytest" in spec
    assert "test_*.py" in spec


def test_render_spec_case_insensitive_language_lookup():
    spec = render_spec(_make_plan(languages=["Python"]))
    assert "pytest" in spec


def test_render_spec_existing_stage_includes_starter_code():
    spec = render_spec(_make_plan(project_stage=ProjectStage.existing))
    assert "## Starter code" in spec


def test_render_spec_greenfield_no_starter_code():
    spec = render_spec(_make_plan(project_stage=ProjectStage.greenfield))
    assert "## Starter code" not in spec


def test_render_spec_contains_overview():
    spec = render_spec(_make_plan())
    assert "## Overview" in spec
    assert "archaeologist" in spec


def test_render_spec_contains_requirements():
    spec = render_spec(_make_plan(tasks=5))
    assert "exactly 5 functional requirements" in spec


def test_render_spec_contains_deliverables():
    spec = render_spec(_make_plan())
    assert "## Deliverables" in spec


def test_render_spec_front_matter_with_technologies():
    spec = render_spec(_make_plan(technologies=["flask", "redis"]))
    assert "technologies:" in spec
    assert "  - flask" in spec
    assert "  - redis" in spec


def test_render_spec_front_matter_no_algorithms():
    spec = render_spec(_make_plan(algorithms=[]))
    assert "algorithms:" not in spec


def test_render_spec_front_matter_no_technologies():
    spec = render_spec(_make_plan(technologies=[]))
    assert "technologies:" not in spec


def test_render_spec_front_matter_closes_with_triple_dash():
    spec = render_spec(_make_plan())
    lines = spec.split("\n")
    assert lines[0] == "---"
    # Find the closing ---
    closing_indices = [i for i, line in enumerate(lines) if line == "---" and i > 0]
    assert len(closing_indices) >= 1


def test_render_spec_definitions_no_algorithms():
    spec = render_spec(_make_plan(algorithms=[]))
    assert "**Algorithms:**" not in spec


def test_render_spec_section_order():
    spec = render_spec(_make_plan())
    sections = [
        "## Definitions",
        "## Overview",
        "## Requirements",
        "## Test specification",
        "## Data files",
        "## Deliverables",
    ]
    positions = [spec.index(s) for s in sections]
    assert positions == sorted(positions), "Sections are out of order"


def test_render_spec_existing_stage_section_order():
    spec = render_spec(_make_plan(project_stage=ProjectStage.existing))
    starter_pos = spec.index("## Starter code")
    deliverables_pos = spec.index("## Deliverables")
    assert starter_pos < deliverables_pos


def test_render_spec_deliverables_existing_stage():
    spec = render_spec(_make_plan(project_stage=ProjectStage.existing))
    assert "Starter code files" in spec


def test_render_spec_deliverables_config_for_python():
    spec = render_spec(_make_plan(languages=["python"]))
    # Deliverables section should mention pyproject.toml
    deliverables_start = spec.index("## Deliverables")
    deliverables = spec[deliverables_start:]
    assert "pyproject.toml" in deliverables


def test_render_spec_unknown_language_fallback():
    spec = render_spec(_make_plan(languages=["cobol"]))
    assert "a suitable test framework" in spec
    assert "test_*" in spec


def test_render_spec_unknown_language_no_config_in_deliverables():
    spec = render_spec(_make_plan(languages=["cobol"]))
    deliverables_start = spec.index("## Deliverables")
    deliverables = spec[deliverables_start:]
    assert "test runner configuration" not in deliverables


def test_render_spec_javascript_framework():
    spec = render_spec(_make_plan(languages=["javascript"]))
    assert "jest" in spec
    assert "*.test.js" in spec
    assert "package.json" in spec


def test_render_spec_go_framework():
    spec = render_spec(_make_plan(languages=["go"]))
    assert "go test" in spec
    assert "*_test.go" in spec
    assert "go.mod" in spec


def test_render_spec_rust_framework():
    spec = render_spec(_make_plan(languages=["rust"]))
    assert "cargo test" in spec
    assert "Cargo.toml" in spec


def test_render_spec_overview_includes_technologies():
    spec = render_spec(_make_plan(technologies=["react", "tailwind"]))
    assert "using react, tailwind" in spec


def test_render_spec_overview_no_algo_note_when_empty():
    spec = render_spec(_make_plan(algorithms=[]))
    overview_start = spec.index("## Overview")
    requirements_start = spec.index("## Requirements")
    overview = spec[overview_start:requirements_start]
    assert "incorporates" not in overview


def test_render_spec_front_matter_with_prompt():
    spec = render_spec(_make_plan(algorithms=[], prompt="Build a bookstore API"))
    assert "prompt: Build a bookstore API" in spec


def test_render_spec_front_matter_no_prompt():
    spec = render_spec(_make_plan(prompt=""))
    assert "prompt:" not in spec


def test_render_spec_definitions_with_prompt():
    spec = render_spec(_make_plan(algorithms=[], prompt="Build a bookstore API"))
    assert "**Prompt:** Build a bookstore API" in spec


def test_render_spec_overview_uses_prompt_when_no_algorithms():
    spec = render_spec(_make_plan(algorithms=[], prompt="Build a bookstore API"))
    overview_start = spec.index("## Overview")
    requirements_start = spec.index("## Requirements")
    overview = spec[overview_start:requirements_start]
    assert "based on the following prompt: Build a bookstore API" in overview


def test_render_spec_overview_prefers_algorithms_over_prompt():
    spec = render_spec(_make_plan(algorithms=["two_sum"], prompt="some prompt"))
    overview_start = spec.index("## Overview")
    requirements_start = spec.index("## Requirements")
    overview = spec[overview_start:requirements_start]
    assert "incorporates" in overview
    assert "based on the following prompt" not in overview


def test_render_spec_each_environment_guidance():
    for env, phrase in [
        (Environment.website, "serve HTML pages"),
        (Environment.cli_app, "accept command-line arguments"),
        (Environment.http_service, "expose HTTP endpoints"),
    ]:
        spec = render_spec(_make_plan(environment=env))
        assert phrase in spec, f"Missing guidance for {env}"
