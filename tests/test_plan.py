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


def test_algorithm_descriptions_no_extra_keys():
    """Every key in ALGORITHM_DESCRIPTIONS must exist in ALGORITHMS."""
    assert set(ALGORITHM_DESCRIPTIONS.keys()) == set(ALGORITHMS)


def test_all_enum_members_are_strings():
    for enum_cls in (Environment, Infrastructure, ProjectStage):
        for member in enum_cls:
            assert isinstance(member, str), f"{member} is not a str"


def test_from_options_creates_plan():
    opts = ExerciseOptions(
        output_dir=Path("/tmp/test"),
        environment=Environment.website,
        infrastructure=Infrastructure.local,
        project_stage=ProjectStage.greenfield,
        languages=["python"],
        technologies=["flask"],
        algorithms=["two_sum"],
        prompt="",
        tasks=3,
        story=DEFAULT_STORY,
        dry_run=False,
    )
    plan = ExercisePlan.from_options(opts)
    assert plan.root == Path("/tmp/test")
    assert plan.environment == Environment.website
    assert plan.infrastructure == Infrastructure.local
    assert plan.project_stage == ProjectStage.greenfield
    assert plan.tasks == 3
    assert plan.languages == ["python"]
    assert plan.technologies == ["flask"]
    assert plan.algorithms == ["two_sum"]
    assert plan.story is DEFAULT_STORY


def test_from_options_empty_technologies():
    opts = ExerciseOptions(
        output_dir=Path("/tmp/test"),
        environment=Environment.cli_app,
        infrastructure=Infrastructure.docker,
        project_stage=ProjectStage.existing,
        languages=["go", "rust"],
        technologies=[],
        algorithms=["two_sum", "coin_change"],
        prompt="",
        tasks=5,
        story=DEFAULT_STORY,
        dry_run=True,
    )
    plan = ExercisePlan.from_options(opts)
    assert plan.technologies == []
    assert plan.languages == ["go", "rust"]
    assert plan.algorithms == ["two_sum", "coin_change"]


def test_add_file_returns_and_stores_file_spec():
    plan = ExercisePlan(
        root=Path("/tmp/test"),
        environment=Environment.cli_app,
        infrastructure=Infrastructure.local,
        project_stage=ProjectStage.greenfield,
        tasks=1,
    )
    spec = plan.add_file("hello.txt", "a greeting", content="hi")
    assert spec.path == Path("hello.txt")
    assert spec.description == "a greeting"
    assert spec.content == "hi"
    assert plan.files == [spec]


def test_add_file_accepts_path_object():
    plan = ExercisePlan(
        root=Path("/tmp/test"),
        environment=Environment.cli_app,
        infrastructure=Infrastructure.local,
        project_stage=ProjectStage.greenfield,
        tasks=1,
    )
    spec = plan.add_file(Path("sub/file.txt"), "nested")
    assert spec.path == Path("sub/file.txt")


def test_add_file_content_defaults_to_none():
    plan = ExercisePlan(
        root=Path("/tmp/test"),
        environment=Environment.cli_app,
        infrastructure=Infrastructure.local,
        project_stage=ProjectStage.greenfield,
        tasks=1,
    )
    spec = plan.add_file("empty.txt", "no content yet")
    assert spec.content is None


def test_add_file_multiple_preserves_order():
    plan = ExercisePlan(
        root=Path("/tmp/test"),
        environment=Environment.cli_app,
        infrastructure=Infrastructure.local,
        project_stage=ProjectStage.greenfield,
        tasks=1,
    )
    a = plan.add_file("a.txt", "first", content="1")
    b = plan.add_file("b.txt", "second", content="2")
    c = plan.add_file("c.txt", "third", content="3")
    assert plan.files == [a, b, c]
