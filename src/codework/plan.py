from __future__ import annotations

import typing
from collections import OrderedDict
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

Algorithm = str

ALGORITHM_CATEGORIES: OrderedDict[str, list[tuple[str, str]]] = OrderedDict([
    ("Arrays & Hashing", [
        ("two_sum", "Two Sum"),
        ("rotate_array", "Rotate Array"),
        ("longest_substring_without_repeating_characters", "Longest Substring Without Repeating Characters"),
        ("product_of_array_except_self", "Product of Array Except Self"),
        ("group_anagrams", "Group Anagrams"),
        ("subarray_sum_equals_k", "Subarray Sum Equals K"),
        ("lru_cache", "LRU Cache"),
    ]),
    ("Two Pointers & Sliding Window", [
        ("three_sum", "3Sum"),
        ("container_with_most_water", "Container With Most Water"),
        ("trapping_rain_water", "Trapping Rain Water"),
        ("min_window_substring", "Min Window Substring"),
        ("linked_list_cycle", "Linked List Cycle"),
        ("happy_number", "Happy Number"),
        ("find_duplicate_number", "Find Duplicate Number"),
    ]),
    ("Linked Lists", [
        ("reverse_a_linked_list", "Reverse a Linked List"),
        ("merge_two_sorted_lists", "Merge Two Sorted Lists"),
        ("detect_cycle", "Detect Cycle"),
        ("copy_list_with_random_pointer", "Copy List with Random Pointer"),
    ]),
    ("Stacks & Queues", [
        ("valid_parentheses", "Valid Parentheses"),
        ("daily_temperatures", "Daily Temperatures"),
        ("largest_rectangle_in_histogram", "Largest Rectangle in Histogram"),
        ("sliding_window_maximum", "Sliding Window Maximum"),
    ]),
    ("Binary Search", [
        ("search_in_rotated_sorted_array", "Search in Rotated Sorted Array"),
        ("find_minimum_in_rotated_sorted_array", "Find Minimum in Rotated Sorted Array"),
        ("koko_eating_bananas", "Koko Eating Bananas"),
        ("ship_packages_in_d_days", "Ship Packages in D Days"),
        ("split_array_largest_sum", "Split Array Largest Sum"),
    ]),
    ("Trees", [
        ("invert_binary_tree", "Invert Binary Tree"),
        ("validate_bst", "Validate BST"),
        ("serialize_deserialize_binary_tree", "Serialize/Deserialize Binary Tree"),
        ("binary_tree_maximum_path_sum", "Binary Tree Maximum Path Sum"),
        ("level_order_traversal", "Level Order Traversal"),
        ("path_sum", "Path Sum"),
        ("diameter_of_binary_tree", "Diameter of Binary Tree"),
    ]),
    ("Heaps", [
        ("kth_largest_element", "Kth Largest Element"),
        ("merge_k_sorted_lists", "Merge K Sorted Lists"),
        ("find_median_from_data_stream", "Find Median from Data Stream"),
    ]),
    ("Tries", [
        ("implement_trie", "Implement Trie"),
        ("word_search_ii", "Word Search II"),
        ("design_search_autocomplete", "Design Search Autocomplete"),
    ]),
    ("Graphs", [
        ("breadth_first_search", "Breadth-First Search"),
        ("depth_first_search", "Depth-First Search"),
        ("number_of_islands", "Number of Islands"),
        ("clone_graph", "Clone Graph"),
        ("course_schedule", "Course Schedule"),
        ("network_delay_time", "Network Delay Time"),
        ("topological_sort", "Topological Sort"),
        ("alien_dictionary", "Alien Dictionary"),
    ]),
    ("Union-Find", [
        ("number_of_connected_components", "Number of Connected Components"),
        ("redundant_connection", "Redundant Connection"),
        ("accounts_merge", "Accounts Merge"),
        ("number_of_provinces", "Number of Provinces"),
        ("longest_consecutive_sequence", "Longest Consecutive Sequence"),
    ]),
    ("Intervals", [
        ("merge_intervals", "Merge Intervals"),
        ("meeting_rooms", "Meeting Rooms"),
        ("non_overlapping_intervals", "Non-Overlapping Intervals"),
    ]),
    ("Dynamic Programming", [
        ("coin_change", "Coin Change"),
        ("house_robber", "House Robber"),
        ("word_break", "Word Break"),
        ("edit_distance", "Edit Distance"),
    ]),
    ("Greedy", [
        ("jump_game", "Jump Game"),
        ("activity_selection", "Activity Selection"),
        ("task_scheduler", "Task Scheduler"),
        ("gas_station", "Gas Station"),
    ]),
    ("Backtracking", [
        ("n_queens", "N-Queens"),
        ("permutations", "Permutations"),
        ("combinations", "Combinations"),
        ("subsets", "Subsets"),
        ("sudoku_solver", "Sudoku Solver"),
        ("word_search", "Word Search"),
    ]),
    ("Bit Manipulation", [
        ("single_number", "Single Number"),
        ("counting_bits", "Counting Bits"),
        ("reverse_bits", "Reverse Bits"),
    ]),
])

ALGORITHMS: tuple[str, ...] = tuple(
    key for problems in ALGORITHM_CATEGORIES.values() for key, _ in problems
)

ALGORITHM_DISPLAY_NAMES: dict[str, str] = {
    key: name
    for problems in ALGORITHM_CATEGORIES.values()
    for key, name in problems
}


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
