"""Tests for interactive prompt wiring (mocked questionary)."""

from pathlib import Path
from unittest.mock import MagicMock, patch

from codework.plan import Environment, Infrastructure, ProjectStage


@patch("codework.interactive.questionary")
def test_prompt_all_returns_exercise_options(mock_q):
    # Set up mock return values for each prompt
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

    from codework.interactive import prompt_all
    opts = prompt_all()

    assert opts["output_dir"] == Path("/tmp/out")
    assert opts["environment"] == Environment.website
    assert opts["infrastructure"] == Infrastructure.docker
    assert opts["project_stage"] == ProjectStage.greenfield
    assert opts["languages"] == ["python", "javascript"]
    assert opts["technologies"] == ["react"]
    assert opts["algorithms"] == ["two_sum"]
    assert opts["tasks"] == 5
    assert opts["dry_run"] is False
