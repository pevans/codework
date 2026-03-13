import argparse
import sys
from pathlib import Path

from codework.interactive import prompt_all
from codework.plan import (
    ALGORITHMS,
    DEFAULT_STORY,
    Environment,
    ExerciseOptions,
    ExercisePlan,
    Infrastructure,
    ProjectStage,
)
from codework.runner import dry_run, execute
from codework.spec import render_spec


def build_parser() -> argparse.ArgumentParser:
    """build_parser returns an argument parser with all of the possible
    command-line arguments that codework can handle."""
    parser = argparse.ArgumentParser(description="Generate code exercises")
    parser.add_argument(
        "-i",
        "--interactive",
        action="store_true",
        help="Collect all options via interactive prompts",
    )
    parser.add_argument(
        "output_dir",
        nargs="?",
        type=Path,
        help="Directory to write the exercise files into",
    )
    parser.add_argument(
        "--environment",
        choices=list(Environment),
        help="Target environment for the exercise (required without -i)",
    )
    parser.add_argument(
        "--infrastructure",
        choices=list(Infrastructure),
        help="Infrastructure target for the exercise (required without -i)",
    )
    parser.add_argument(
        "--project-stage",
        choices=list(ProjectStage),
        help="Project stage for the exercise (required without -i)",
    )
    parser.add_argument(
        "--language",
        dest="languages",
        action="append",
        metavar="LANGUAGE",
        help="Programming language for the exercise (required without -i; may be repeated)",
    )
    parser.add_argument(
        "--technology",
        dest="technologies",
        action="append",
        metavar="TECHNOLOGY",
        default=[],
        help="Framework or library used in the exercise (may be repeated)",
    )
    parser.add_argument(
        "--algorithm",
        dest="algorithms",
        action="append",
        choices=ALGORITHMS,
        metavar="ALGORITHM",
        default=[],
        help=f"Algorithm to test with (may be repeated); choices: {', '.join(ALGORITHMS)}",
    )
    parser.add_argument(
        "--prompt",
        type=str,
        default="",
        help="Free-form prompt describing the exercise topic (used in place of --algorithm)",
    )
    parser.add_argument(
        "--tasks",
        type=int,
        help="Number of tasks in the exercise (required without -i)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would be written without touching the filesystem",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    try:
        if args.interactive:
            opts = prompt_all()
            # CLI flag takes precedence over the in-prompt answer.
            if args.dry_run:
                opts["dry_run"] = True
        else:
            missing = []
            if args.output_dir is None:
                missing.append("output_dir (positional)")
            if args.environment is None:
                missing.append("--environment")
            if args.infrastructure is None:
                missing.append("--infrastructure")
            if args.project_stage is None:
                missing.append("--project-stage")
            if not args.languages:
                missing.append("--language")
            if not args.algorithms and not args.prompt:
                missing.append("--algorithm or --prompt")
            if args.tasks is None:
                missing.append("--tasks")
            if missing:
                parser.error(
                    "the following arguments are required: "
                    + ", ".join(missing)
                    + " (or pass -i / --interactive)"
                )
            opts = ExerciseOptions(
                output_dir=args.output_dir,
                environment=Environment(args.environment),
                infrastructure=Infrastructure(args.infrastructure),
                project_stage=ProjectStage(args.project_stage),
                languages=args.languages,
                technologies=args.technologies,
                algorithms=args.algorithms,
                prompt=args.prompt,
                tasks=args.tasks,
                story=DEFAULT_STORY,
                dry_run=args.dry_run,
            )

        plan = ExercisePlan.from_options(opts)

        plan.add_file(
            path="SPEC.md",
            description="Machine-readable spec for LLM-assisted exercise generation",
            content=render_spec(plan),
        )

        if opts["dry_run"]:
            dry_run(plan)
        else:
            execute(plan)
    except KeyboardInterrupt:
        raise SystemExit(0)
    except (OSError, RuntimeError) as e:
        print(f"error: {e}", file=sys.stderr)
        raise SystemExit(1)
