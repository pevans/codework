"""Interactive prompts for collecting exercise options."""

from __future__ import annotations

from pathlib import Path

import questionary

from codework.plan import (
    ALGORITHMS,
    DEFAULT_STORY,
    ENVIRONMENTS,
    INFRASTRUCTURES,
    LENGTHS,
    PROJECT_STAGES,
    ExerciseOptions,
)


def prompt_all() -> ExerciseOptions:
    """Interactively prompt for all exercise options.

    Raises KeyboardInterrupt if the user cancels (Ctrl-C / Ctrl-D).
    """
    output_dir = questionary.path(
        "Output directory:",
        only_directories=True,
    ).unsafe_ask()

    environment = questionary.select(
        "Environment:",
        choices=list(ENVIRONMENTS),
    ).unsafe_ask()

    infrastructure = questionary.select(
        "Infrastructure:",
        choices=list(INFRASTRUCTURES),
    ).unsafe_ask()

    project_stage = questionary.select(
        "Project stage:",
        choices=list(PROJECT_STAGES),
    ).unsafe_ask()

    languages_raw = questionary.text(
        "Languages (comma-separated):",
        validate=lambda v: bool(v.strip()) or "At least one language is required.",
    ).unsafe_ask()
    languages = [lang.strip() for lang in languages_raw.split(",") if lang.strip()]

    technologies_raw = questionary.text(
        "Technologies (comma-separated; leave blank to skip):",
    ).unsafe_ask()
    technologies = [t.strip() for t in technologies_raw.split(",") if t.strip()]

    algorithms = questionary.checkbox(
        "Algorithms:",
        choices=list(ALGORITHMS),
    ).unsafe_ask()

    length = questionary.select(
        "Length:",
        choices=list(LENGTHS),
    ).unsafe_ask()

    dry_run = questionary.confirm(
        "Dry run?",
        default=False,
    ).unsafe_ask()

    return ExerciseOptions(
        output_dir=Path(output_dir),
        environment=environment,
        infrastructure=infrastructure,
        project_stage=project_stage,
        languages=languages,
        technologies=technologies,
        algorithms=algorithms,
        length=length,
        story=DEFAULT_STORY,
        dry_run=dry_run,
    )
