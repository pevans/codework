"""Tests for interactive prompt wiring (mocked questionary)."""

from pathlib import Path
from unittest.mock import patch

from codework.plan import (
    Environment,
    FramingStory,
    Infrastructure,
    ProjectStage,
)


def _setup_mock(mock_q, **overrides):
    """Configure mock_q with sensible defaults, then apply overrides."""
    mock_q.path.return_value.unsafe_ask.return_value = "/tmp/out"
    mock_q.select.return_value.unsafe_ask.side_effect = [
        Environment.website,
        Infrastructure.docker,
        ProjectStage.greenfield,
    ]
    mock_q.text.return_value.unsafe_ask.side_effect = [
        "python, javascript",  # languages
        "react",               # technologies
        "5",                   # tasks
    ]
    mock_q.checkbox.return_value.unsafe_ask.return_value = ["two_sum"]
    mock_q.confirm.return_value.unsafe_ask.return_value = False

    for key, value in overrides.items():
        parts = key.split(".")
        obj = mock_q
        for part in parts[:-1]:
            obj = getattr(obj, part)
        setattr(obj, parts[-1], value)


@patch("codework.interactive.questionary")
def test_prompt_all_returns_exercise_options(mock_q):
    _setup_mock(mock_q)

    from codework.interactive import prompt_all
    opts = prompt_all()

    assert isinstance(opts["output_dir"], Path)
    assert isinstance(opts["environment"], Environment)
    assert isinstance(opts["infrastructure"], Infrastructure)
    assert isinstance(opts["project_stage"], ProjectStage)
    assert isinstance(opts["languages"], list)
    assert len(opts["languages"]) > 0
    assert isinstance(opts["technologies"], list)
    assert isinstance(opts["algorithms"], list)
    assert len(opts["algorithms"]) > 0
    assert isinstance(opts["tasks"], int)
    assert opts["tasks"] > 0
    assert isinstance(opts["dry_run"], bool)


@patch("codework.interactive.questionary")
def test_prompt_all_passes_through_select_values(mock_q):
    _setup_mock(mock_q)

    from codework.interactive import prompt_all
    opts = prompt_all()

    assert opts["environment"] == Environment.website
    assert opts["infrastructure"] == Infrastructure.docker
    assert opts["project_stage"] == ProjectStage.greenfield


@patch("codework.interactive.questionary")
def test_prompt_all_converts_output_dir_to_path(mock_q):
    _setup_mock(mock_q)

    from codework.interactive import prompt_all
    opts = prompt_all()

    assert opts["output_dir"] == Path("/tmp/out")


@patch("codework.interactive.questionary")
def test_prompt_all_has_a_story(mock_q):
    _setup_mock(mock_q)

    from codework.interactive import prompt_all
    opts = prompt_all()

    assert isinstance(opts["story"], FramingStory)
    assert opts["story"].name
    assert opts["story"].premise
    assert opts["story"].role
    assert opts["story"].motivation


@patch("codework.interactive.questionary")
def test_prompt_all_empty_technologies(mock_q):
    _setup_mock(mock_q, **{
        "text.return_value.unsafe_ask.side_effect": [
            "python",  # languages
            "",         # technologies -- blank
            "3",        # tasks
        ],
    })

    from codework.interactive import prompt_all
    opts = prompt_all()

    assert opts["technologies"] == []


@patch("codework.interactive.questionary")
def test_prompt_all_dry_run_mirrors_confirm(mock_q):
    _setup_mock(mock_q, **{
        "confirm.return_value.unsafe_ask.return_value": True,
    })

    from codework.interactive import prompt_all
    opts = prompt_all()

    assert opts["dry_run"] is True


@patch("codework.interactive.questionary")
def test_prompt_all_single_language_no_comma(mock_q):
    _setup_mock(mock_q, **{
        "text.return_value.unsafe_ask.side_effect": [
            "python",  # single language, no comma
            "react",   # technologies
            "3",       # tasks
        ],
    })

    from codework.interactive import prompt_all
    opts = prompt_all()

    assert opts["languages"] == ["python"]


@patch("codework.interactive.questionary")
def test_prompt_all_languages_strips_whitespace(mock_q):
    _setup_mock(mock_q, **{
        "text.return_value.unsafe_ask.side_effect": [
            "  python  ,  go  ",  # extra whitespace
            "",                   # technologies
            "2",                  # tasks
        ],
    })

    from codework.interactive import prompt_all
    opts = prompt_all()

    assert opts["languages"] == ["python", "go"]


@patch("codework.interactive.questionary")
def test_prompt_all_languages_trailing_comma_ignored(mock_q):
    _setup_mock(mock_q, **{
        "text.return_value.unsafe_ask.side_effect": [
            "python,",  # trailing comma
            "",          # technologies
            "1",         # tasks
        ],
    })

    from codework.interactive import prompt_all
    opts = prompt_all()

    assert opts["languages"] == ["python"]


@patch("codework.interactive.questionary")
def test_prompt_all_multiple_algorithms(mock_q):
    _setup_mock(mock_q, **{
        "checkbox.return_value.unsafe_ask.return_value": [
            "two_sum",
            "coin_change",
            "n_queens",
        ],
    })

    from codework.interactive import prompt_all
    opts = prompt_all()

    assert opts["algorithms"] == ["two_sum", "coin_change", "n_queens"]


@patch("codework.interactive.questionary")
def test_prompt_all_parses_tasks_as_int(mock_q):
    _setup_mock(mock_q, **{
        "text.return_value.unsafe_ask.side_effect": [
            "python",  # languages
            "",         # technologies
            "  7  ",    # tasks with whitespace
        ],
    })

    from codework.interactive import prompt_all
    opts = prompt_all()

    assert opts["tasks"] == 7
    assert isinstance(opts["tasks"], int)
