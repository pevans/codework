"""Interactive prompts for collecting exercise options."""

from __future__ import annotations

from pathlib import Path

import questionary
from questionary import Choice, Separator

from codework.plan import (
    ALGORITHM_CATEGORIES,
    DEFAULT_STORY,
    Environment,
    ExerciseOptions,
    Infrastructure,
    ProjectStage,
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
        choices=[Choice(title=e.display_name, value=e) for e in Environment],
    ).unsafe_ask()

    infrastructure = questionary.select(
        "Infrastructure:",
        choices=[Choice(title=i.display_name, value=i) for i in Infrastructure],
    ).unsafe_ask()

    project_stage = questionary.select(
        "Project stage:",
        choices=[Choice(title=s.display_name, value=s) for s in ProjectStage],
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

    algorithm_choices: list[Separator | Choice] = []
    for category, problems in ALGORITHM_CATEGORIES.items():
        algorithm_choices.append(Separator(f"── {category} ──"))
        for key, display_name in problems:
            algorithm_choices.append(Choice(title=display_name, value=key))

    algorithms = questionary.checkbox(
        "Algorithms:",
        choices=algorithm_choices,
        instruction="(Space to select, Enter to confirm)",
        validate=lambda v: len(v) > 0 or "At least one algorithm is required.",
    ).unsafe_ask()

    tasks_raw = questionary.text(
        "Number of tasks:",
        validate=lambda v: True if (v.strip().isdigit() and int(v.strip()) > 0) else "Enter a positive integer.",
    ).unsafe_ask()
    tasks = int(tasks_raw.strip())

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
        tasks=tasks,
        story=DEFAULT_STORY,
        dry_run=dry_run,
    )
