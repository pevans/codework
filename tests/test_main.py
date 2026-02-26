"""Tests for argument parsing and validation in main."""

import subprocess
import sys


def _run_codework(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "-c", "from codework.main import main; main()", *args],
        capture_output=True,
        text=True,
    )


def test_help_flag():
    result = _run_codework("--help")
    assert result.returncode == 0
    assert "Generate code exercises" in result.stdout


def test_missing_required_args_without_interactive():
    result = _run_codework()
    assert result.returncode != 0
    assert "output_dir" in result.stderr
    assert "--environment" in result.stderr
    assert "--algorithm" in result.stderr


def test_missing_algorithm_is_reported():
    result = _run_codework(
        "/tmp/out",
        "--environment", "website",
        "--infrastructure", "local",
        "--project-stage", "greenfield",
        "--language", "python",
        "--tasks", "3",
    )
    assert result.returncode != 0
    assert "--algorithm" in result.stderr


def test_interactive_flag_accepted():
    result = _run_codework("--help")
    assert "--interactive" in result.stdout or "-i" in result.stdout
