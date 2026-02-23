import sys

from codework.plan import ExercisePlan


def dry_run(plan: ExercisePlan) -> None:
    """Print what would be written without touching the filesystem."""
    print(f"Dry run -- root: {plan.root}\n")
    for spec in plan.files:
        dest = plan.root / spec.path
        print(f"=== Would write: {dest} ===")
        print(f"# {spec.description}")
        if spec.content is not None:
            print(spec.content)
        else:
            print("(no content yet)")
        print()


def execute(plan: ExercisePlan) -> None:
    """Write all files in the plan to the filesystem.

    Raises RuntimeError if any files were skipped due to missing content,
    since a partial write leaves the exercise directory in an incomplete state.
    """
    plan.root.mkdir(parents=True, exist_ok=True)
    skipped: list[str] = []
    for spec in plan.files:
        dest = plan.root / spec.path
        dest.parent.mkdir(parents=True, exist_ok=True)
        if spec.content is not None:
            dest.write_text(spec.content)
            print(f"Wrote: {dest}")
        else:
            print(f"warning: skipped (no content): {dest}", file=sys.stderr)
            skipped.append(str(dest))
    if skipped:
        raise RuntimeError(
            f"{len(skipped)} file(s) skipped due to missing content: {', '.join(skipped)}"
        )
