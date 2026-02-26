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

    Raises RuntimeError before writing anything if any FileSpec has no content.
    """
    missing = [str(spec.path) for spec in plan.files if spec.content is None]
    if missing:
        raise RuntimeError(
            f"{len(missing)} file(s) have no content: {', '.join(missing)}"
        )
    plan.root.mkdir(parents=True, exist_ok=True)
    for spec in plan.files:
        dest = plan.root / spec.path
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(spec.content)  # type: ignore[arg-type]
        print(f"Wrote: {dest}")
