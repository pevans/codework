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
        story=DEFAULT_STORY,
    )
    defaults.update(overrides)
    return ExercisePlan(**defaults)


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
