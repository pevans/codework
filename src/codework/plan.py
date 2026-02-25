from __future__ import annotations

import typing
from typing import Literal
from dataclasses import dataclass, field
from pathlib import Path
from typing import TypedDict

Environment = Literal["website", "cli_app", "http_service"]
ENVIRONMENTS: tuple[Environment, ...] = typing.get_args(Environment)

Infrastructure = Literal["local", "docker", "cloud"]
INFRASTRUCTURES: tuple[Infrastructure, ...] = typing.get_args(Infrastructure)

ProjectStage = Literal["greenfield", "existing"]
PROJECT_STAGES: tuple[ProjectStage, ...] = typing.get_args(ProjectStage)

Algorithm = Literal["breadth_first_search", "depth_first_search"]
ALGORITHMS: tuple[Algorithm, ...] = typing.get_args(Algorithm)


@dataclass(frozen=True)
class FramingStory:
    """Narrative wrapper that gives an exercise a thematic context."""

    name: str
    premise: str
    role: str
    motivation: str


DEFAULT_STORY = FramingStory(
    name="archaeology",
    premise="You've just arrived at a remote dig site where ancient artifacts have been unearthed, and the research team needs software to catalog and analyze the findings.",
    role="an archaeologist",
    motivation="Accurate cataloging is critical -- mislabeled artifacts could rewrite history, and the funding agency demands a working demo before the next grant cycle.",
)


class ExerciseOptions(TypedDict):
    output_dir: Path
    environment: Environment
    infrastructure: Infrastructure
    project_stage: ProjectStage
    languages: list[str]
    technologies: list[str]
    algorithms: list[Algorithm]
    tasks: int
    story: FramingStory
    dry_run: bool


@dataclass
class FileSpec:
    """A single file to be written as part of an exercise.

    `path` is relative to the exercise root.
    `description` captures the intent of the file.
    `content` is the literal text to write; None means not yet generated.
    """

    path: Path
    description: str
    content: str | None = None


@dataclass
class ExercisePlan:
    """A plan for generating a code exercise under `root`."""

    root: Path
    environment: Environment
    infrastructure: Infrastructure
    project_stage: ProjectStage
    tasks: int
    languages: list[str] = field(default_factory=list)
    technologies: list[str] = field(default_factory=list)
    algorithms: list[Algorithm] = field(default_factory=list)
    story: FramingStory = field(default_factory=lambda: DEFAULT_STORY)
    files: list[FileSpec] = field(default_factory=list)

    def add_file(
        self,
        path: str | Path,
        description: str,
        content: str | None = None,
    ) -> FileSpec:
        spec = FileSpec(path=Path(path), description=description, content=content)
        self.files.append(spec)
        return spec
