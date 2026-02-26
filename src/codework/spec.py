"""Render SPEC.md content from an ExercisePlan."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from codework.plan import ExercisePlan

# Maps language names to their conventional test frameworks and file patterns.
_TEST_FRAMEWORKS: dict[str, tuple[str, str, str]] = {
    # (framework, test file pattern, config file)
    "python": ("pytest", "test_*.py", "pyproject.toml"),
    "javascript": ("jest", "*.test.js", "package.json"),
    "typescript": ("jest", "*.test.ts", "package.json"),
    "ruby": ("rspec", "*_spec.rb", "Gemfile"),
    "go": ("go test", "*_test.go", "go.mod"),
    "rust": ("cargo test", "*_test.rs", "Cargo.toml"),
    "java": ("junit", "*Test.java", "pom.xml"),
}

_DEFAULT_TEST_FRAMEWORK = ("a suitable test framework", "test_*", "")



def render_spec(plan: ExercisePlan) -> str:
    """Return the full SPEC.md content for the given plan."""
    parts = [_front_matter(plan), _overview(plan), _requirements(plan),
             _test_specification(plan), _data_files(plan)]
    if plan.project_stage == "existing":
        parts.append(_starter_code(plan))
    parts.append(_deliverables(plan))
    return "\n".join(parts)


def _front_matter(plan: ExercisePlan) -> str:
    lines = ["---"]
    lines.append(f"environment: {plan.environment}")
    lines.append(f"infrastructure: {plan.infrastructure}")
    lines.append(f"project_stage: {plan.project_stage}")
    lines.append(f"tasks: {plan.tasks}")
    lines.append("languages:")
    for lang in plan.languages:
        lines.append(f"  - {lang}")
    if plan.technologies:
        lines.append("technologies:")
        for tech in plan.technologies:
            lines.append(f"  - {tech}")
    if plan.algorithms:
        lines.append("algorithms:")
        for algo in plan.algorithms:
            lines.append(f"  - {algo}")
    lines.append(f"story: {plan.story.name}")
    lines.append("---")
    lines.append("")
    return "\n".join(lines)


def _overview(plan: ExercisePlan) -> str:
    langs = ", ".join(plan.languages)
    algo_note = ""
    if plan.algorithms:
        algo_note = f" that incorporates {', '.join(plan.algorithms)}"
    tech_note = ""
    if plan.technologies:
        tech_note = f" using {', '.join(plan.technologies)}"
    story = plan.story
    return (
        "## Overview\n"
        "\n"
        f"The exerciser is {story.role}. {story.premise} "
        f"{story.motivation}\n"
        "\n"
        f"Write a one-paragraph scenario description for a {plan.tasks}-task "
        f"{plan.environment} exercise in {langs}{tech_note}{algo_note}. "
        "Describe the context, what the exerciser will build or fix, and "
        "why it matters. Frame the narrative around the role and premise above.\n"
    )


def _requirements(plan: ExercisePlan) -> str:
    count = plan.tasks
    env_guidance = {
        "website": "serve HTML pages and handle user interactions in the browser",
        "cli_app": "accept command-line arguments and produce correct stdout/stderr output",
        "http_service": "expose HTTP endpoints and return correct status codes and response bodies",
    }
    guidance = env_guidance.get(plan.environment, "function correctly")
    return (
        "## Requirements\n"
        "\n"
        f"Generate exactly {count} functional requirements as a bulleted list. "
        f"Each requirement must be testable via black-box tests. "
        f"The application should {guidance}.\n"
    )


def _test_specification(plan: ExercisePlan) -> str:
    primary_lang = plan.languages[0]
    framework, pattern, config = _TEST_FRAMEWORKS.get(
        primary_lang, _DEFAULT_TEST_FRAMEWORK
    )

    lines = [
        "## Test specification",
        "",
        "Write black-box tests that verify the requirements above. "
        "Tests must not depend on internal implementation details.",
        "",
        f"- **Test framework:** {framework}",
        f"- **Test file pattern:** `{pattern}`",
    ]
    if config:
        lines.append(f"- **Test runner config:** `{config}`")
    lines.append(
        "- **Test categories:** include happy-path, edge-case, "
        "and error-handling tests"
    )
    lines.append("")
    return "\n".join(lines)


def _data_files(plan: ExercisePlan) -> str:
    return (
        "## Data files\n"
        "\n"
        "Generate any data files the exerciser will need to run the exercise "
        "(e.g. sample input files, seed data, fixture JSON, CSV datasets). "
        "These files must be ready to use -- the exerciser should not have to "
        "create or find test data on their own.\n"
    )


def _starter_code(plan: ExercisePlan) -> str:
    return (
        "## Starter code\n"
        "\n"
        "Generate starter code for the exerciser to begin with. "
        "The code should be structurally complete but functionally incomplete:\n"
        "\n"
        "- Include TODO comments marking where the exerciser must add or fix code\n"
        "- Pre-implement boilerplate (imports, configuration, entry point) "
        "so the exerciser can focus on the core logic\n"
        "- The starter code must be syntactically valid and runnable "
        "(tests should fail, not crash)\n"
    )


def _deliverables(plan: ExercisePlan) -> str:
    primary_lang = plan.languages[0]
    _, pattern, config = _TEST_FRAMEWORKS.get(
        primary_lang, _DEFAULT_TEST_FRAMEWORK
    )

    lines = [
        "## Deliverables",
        "",
        "Produce the following files:",
        "",
        "- `README.md` -- human-readable exercise instructions for the exerciser",
        f"- Test files (`{pattern}`) -- black-box tests for every requirement",
    ]
    if config:
        lines.append(f"- `{config}` -- test runner configuration")
    lines.append(
        "- Data files -- sample inputs, seed data, or fixtures as described "
        "in the Data files section"
    )
    if plan.project_stage == "existing":
        lines.append(
            "- Starter code files -- scaffolded source as described "
            "in the Starter code section"
        )
    lines.append("")
    return "\n".join(lines)
