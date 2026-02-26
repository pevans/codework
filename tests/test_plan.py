"""Tests for plan data integrity."""

from pathlib import Path

from codework.plan import (
    ALGORITHM_CATEGORIES,
    ALGORITHM_DESCRIPTIONS,
    ALGORITHM_DISPLAY_NAMES,
    ALGORITHMS,
    DEFAULT_STORY,
    Environment,
    ExerciseOptions,
    ExercisePlan,
    Infrastructure,
    ProjectStage,
)


def test_all_algorithms_have_descriptions():
    for algo in ALGORITHMS:
        assert algo in ALGORITHM_DESCRIPTIONS, f"{algo} missing from ALGORITHM_DESCRIPTIONS"


def test_all_algorithms_have_display_names():
    for algo in ALGORITHMS:
        assert algo in ALGORITHM_DISPLAY_NAMES, f"{algo} missing from ALGORITHM_DISPLAY_NAMES"


def test_all_algorithms_appear_in_exactly_one_category():
    seen: dict[str, str] = {}
    for category, problems in ALGORITHM_CATEGORIES.items():
        for key, _ in problems:
            assert key not in seen, f"{key} appears in both '{seen[key]}' and '{category}'"
            seen[key] = category
    assert set(seen.keys()) == set(ALGORITHMS)


def test_environment_enum_has_display_names_and_descriptions():
    for member in Environment:
        assert member.display_name, f"{member} has no display_name"
        assert member.description, f"{member} has no description"


def test_infrastructure_enum_has_display_names_and_descriptions():
    for member in Infrastructure:
        assert member.display_name, f"{member} has no display_name"
        assert member.description, f"{member} has no description"


def test_project_stage_enum_has_display_names_and_descriptions():
    for member in ProjectStage:
        assert member.display_name, f"{member} has no display_name"
        assert member.description, f"{member} has no description"


def test_enum_string_values():
    assert str(Environment.website) == "website"
    assert str(Infrastructure.docker) == "docker"
    assert str(ProjectStage.greenfield) == "greenfield"


def test_from_options_creates_plan():
    opts = ExerciseOptions(
        output_dir=Path("/tmp/test"),
        environment=Environment.website,
        infrastructure=Infrastructure.local,
        project_stage=ProjectStage.greenfield,
        languages=["python"],
        technologies=["flask"],
        algorithms=["two_sum"],
        tasks=3,
        story=DEFAULT_STORY,
        dry_run=False,
    )
    plan = ExercisePlan.from_options(opts)
    assert plan.root == Path("/tmp/test")
    assert plan.environment == Environment.website
    assert plan.tasks == 3
    assert plan.languages == ["python"]
    assert plan.algorithms == ["two_sum"]
