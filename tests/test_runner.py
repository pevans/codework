"""Tests for execute() and dry_run()."""

from pathlib import Path

import pytest

from codework.plan import (
    DEFAULT_STORY,
    Environment,
    ExercisePlan,
    Infrastructure,
    ProjectStage,
)
from codework.runner import dry_run, execute


def _make_plan(root: Path, **overrides) -> ExercisePlan:
    defaults = dict(
        root=root,
        environment=Environment.cli_app,
        infrastructure=Infrastructure.local,
        project_stage=ProjectStage.greenfield,
        tasks=3,
        languages=["python"],
        story=DEFAULT_STORY,
    )
    defaults.update(overrides)
    return ExercisePlan(**defaults)


def test_execute_writes_files(tmp_path: Path):
    plan = _make_plan(tmp_path / "out")
    plan.add_file("hello.txt", "greeting", content="Hello, world!")
    plan.add_file("sub/nested.txt", "nested file", content="Nested content")
    execute(plan)
    assert (tmp_path / "out" / "hello.txt").read_text() == "Hello, world!"
    assert (tmp_path / "out" / "sub" / "nested.txt").read_text() == "Nested content"


def test_execute_raises_before_writing_if_content_missing(tmp_path: Path):
    plan = _make_plan(tmp_path / "out")
    plan.add_file("good.txt", "has content", content="ok")
    plan.add_file("bad.txt", "no content")
    with pytest.raises(RuntimeError, match="no content"):
        execute(plan)
    assert not (tmp_path / "out" / "good.txt").exists()


def test_dry_run_does_not_write_files(tmp_path: Path, capsys):
    plan = _make_plan(tmp_path / "out")
    plan.add_file("hello.txt", "greeting", content="Hello!")
    dry_run(plan)
    assert not (tmp_path / "out").exists()
    captured = capsys.readouterr()
    assert "Would write" in captured.out
    assert "Hello!" in captured.out
