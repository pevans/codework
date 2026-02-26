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
    return ExercisePlan(**defaults)  # type: ignore[arg-type]


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


def test_dry_run_no_content_shows_placeholder(tmp_path: Path, capsys):
    plan = _make_plan(tmp_path / "out")
    plan.add_file("stub.txt", "placeholder file")
    dry_run(plan)
    captured = capsys.readouterr()
    assert "(no content yet)" in captured.out


def test_dry_run_output_includes_root_and_description(tmp_path: Path, capsys):
    plan = _make_plan(tmp_path / "out")
    plan.add_file("hello.txt", "greeting", content="Hello!")
    dry_run(plan)
    captured = capsys.readouterr()
    assert f"Dry run -- root: {tmp_path / 'out'}" in captured.out
    assert "# greeting" in captured.out


def test_execute_prints_wrote_lines(tmp_path: Path, capsys):
    plan = _make_plan(tmp_path / "out")
    plan.add_file("a.txt", "first", content="A")
    plan.add_file("b.txt", "second", content="B")
    execute(plan)
    captured = capsys.readouterr()
    assert captured.out.count("Wrote:") == 2
    assert str(tmp_path / "out" / "a.txt") in captured.out
    assert str(tmp_path / "out" / "b.txt") in captured.out


def test_execute_creates_deeply_nested_root(tmp_path: Path):
    deep_root = tmp_path / "a" / "b" / "c" / "d"
    plan = _make_plan(deep_root)
    plan.add_file("file.txt", "deep", content="deep content")
    execute(plan)
    assert (deep_root / "file.txt").read_text() == "deep content"


def test_execute_with_empty_files_list(tmp_path: Path):
    plan = _make_plan(tmp_path / "out")
    execute(plan)
    assert (tmp_path / "out").is_dir()


def test_execute_root_already_exists(tmp_path: Path):
    root = tmp_path / "out"
    root.mkdir()
    plan = _make_plan(root)
    plan.add_file("file.txt", "test", content="ok")
    execute(plan)
    assert (root / "file.txt").read_text() == "ok"


def test_execute_multiple_missing_files_error(tmp_path: Path):
    plan = _make_plan(tmp_path / "out")
    plan.add_file("a.txt", "first")
    plan.add_file("b.txt", "second")
    with pytest.raises(RuntimeError, match="2 file\\(s\\)") as exc_info:
        execute(plan)
    assert "a.txt" in str(exc_info.value)
    assert "b.txt" in str(exc_info.value)
