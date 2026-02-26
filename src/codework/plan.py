from __future__ import annotations

from collections import OrderedDict
from enum import StrEnum
from dataclasses import dataclass, field
from pathlib import Path
from typing import TypedDict


class _DescriptiveEnum(StrEnum):
    """Base for enums that carry a display name and description."""

    _display_name: str
    _description: str

    def __new__(cls, value: str, display_name: str, description: str) -> _DescriptiveEnum:
        obj = str.__new__(cls, value)
        obj._value_ = value
        obj._display_name = display_name
        obj._description = description
        return obj

    @property
    def display_name(self) -> str:
        return self._display_name

    @property
    def description(self) -> str:
        return self._description


class Environment(_DescriptiveEnum):
    website = (
        "website",
        "Website",
        "A browser-based application that serves HTML pages and handles user interactions in the browser.",
    )
    cli_app = (
        "cli_app",
        "CLI Application",
        "A command-line program that accepts arguments and flags, reads from stdin or files, and produces output on stdout/stderr.",
    )
    http_service = (
        "http_service",
        "HTTP Service",
        "A backend service that exposes HTTP/REST endpoints and returns JSON or other structured responses.",
    )


class Infrastructure(_DescriptiveEnum):
    local = (
        "local",
        "Local",
        "Runs directly on the developer's machine with no containerization or remote deployment.",
    )
    docker = (
        "docker",
        "Docker",
        "Packaged as a Docker container with a Dockerfile and optional docker-compose configuration.",
    )
    cloud = (
        "cloud",
        "Cloud",
        "Deployed to a cloud platform (e.g. AWS, GCP, or Azure) with infrastructure-as-code or platform-specific configuration.",
    )


class ProjectStage(_DescriptiveEnum):
    greenfield = (
        "greenfield",
        "Greenfield",
        "The exerciser starts from scratch -- no existing code is provided, and they must build the entire project.",
    )
    existing = (
        "existing",
        "Existing Codebase",
        "The exerciser receives a partially-built project with starter code and must extend, fix, or complete it.",
    )

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

ALGORITHM_DESCRIPTIONS: dict[str, str] = {
    # Arrays & Hashing
    "two_sum": "Given an array of integers and a target, find two numbers that add up to the target.",
    "rotate_array": "Rotate an array of n elements to the right by k steps.",
    "longest_substring_without_repeating_characters": "Find the length of the longest substring without repeating characters.",
    "product_of_array_except_self": "Return an array where each element is the product of all other elements, without using division.",
    "group_anagrams": "Group strings that are anagrams of each other.",
    "subarray_sum_equals_k": "Find the total number of contiguous subarrays whose sum equals a given value k.",
    "lru_cache": "Design a data structure that supports get and put operations with least-recently-used eviction.",
    # Two Pointers & Sliding Window
    "three_sum": "Find all unique triplets in an array that sum to zero.",
    "container_with_most_water": "Find two lines that, together with the x-axis, form a container holding the most water.",
    "trapping_rain_water": "Compute how much water can be trapped between bars of varying heights after rain.",
    "min_window_substring": "Find the smallest substring that contains all characters of a given pattern.",
    "happy_number": "Determine whether repeatedly summing the squares of a number's digits eventually reaches 1.",
    "find_duplicate_number": "Find the duplicate in an array of n+1 integers in the range [1, n] without modifying the array.",
    # Linked Lists
    "reverse_a_linked_list": "Reverse a singly linked list iteratively or recursively.",
    "merge_two_sorted_lists": "Merge two sorted linked lists into one sorted linked list.",
    "detect_cycle": "Detect whether a linked list has a cycle using the fast/slow pointer technique and find the cycle's start node.",
    "copy_list_with_random_pointer": "Deep-copy a linked list where each node has an additional pointer to a random node.",
    # Stacks & Queues
    "valid_parentheses": "Determine if a string of brackets is properly nested and balanced.",
    "daily_temperatures": "For each day's temperature, find how many days until a warmer temperature.",
    "largest_rectangle_in_histogram": "Find the area of the largest rectangle that fits within a histogram's bars.",
    "sliding_window_maximum": "Find the maximum value in each sliding window of size k across an array.",
    # Binary Search
    "search_in_rotated_sorted_array": "Search for a target value in a sorted array that has been rotated at an unknown pivot.",
    "find_minimum_in_rotated_sorted_array": "Find the minimum element in a sorted array that has been rotated.",
    "koko_eating_bananas": "Find the minimum eating speed so that all banana piles are finished within h hours.",
    "ship_packages_in_d_days": "Find the minimum ship capacity to deliver all packages within d days.",
    "split_array_largest_sum": "Split an array into m subarrays to minimize the largest subarray sum.",
    # Trees
    "invert_binary_tree": "Swap the left and right children of every node in a binary tree.",
    "validate_bst": "Determine whether a binary tree satisfies the binary search tree property.",
    "serialize_deserialize_binary_tree": "Convert a binary tree to a string representation and reconstruct it.",
    "binary_tree_maximum_path_sum": "Find the path with the maximum sum between any two nodes in a binary tree.",
    "level_order_traversal": "Visit all nodes of a binary tree level by level, left to right.",
    "path_sum": "Determine if a binary tree has a root-to-leaf path whose node values sum to a target.",
    "diameter_of_binary_tree": "Find the length of the longest path between any two nodes in a binary tree.",
    # Heaps
    "kth_largest_element": "Find the kth largest element in an unsorted array efficiently.",
    "merge_k_sorted_lists": "Merge k sorted linked lists into a single sorted list.",
    "find_median_from_data_stream": "Design a structure that supports adding numbers and finding the current median efficiently.",
    # Tries
    "implement_trie": "Build a prefix tree supporting insert, search, and startsWith operations.",
    "word_search_ii": "Find all words from a dictionary that can be formed on a letter board by tracing adjacent cells.",
    "design_search_autocomplete": "Design a system that suggests top completions as a user types a search query.",
    # Graphs
    "breadth_first_search": "Traverse a graph level by level from a starting node using a queue.",
    "depth_first_search": "Traverse a graph by exploring as far as possible along each branch before backtracking.",
    "number_of_islands": "Count the number of connected land regions in a 2D grid of land and water cells.",
    "clone_graph": "Create a deep copy of an undirected graph, preserving its structure.",
    "course_schedule": "Determine whether all courses can be finished given prerequisite relationships (cycle detection).",
    "network_delay_time": "Find the time for a signal to reach all nodes in a weighted directed graph (shortest paths).",
    "topological_sort": "Order directed-graph nodes so every edge goes from earlier to later in the ordering.",
    "alien_dictionary": "Derive the character ordering of an alien language from a sorted list of words.",
    # Union-Find
    "number_of_connected_components": "Count the number of connected components in an undirected graph.",
    "redundant_connection": "Find the edge that, if removed, makes an undirected graph a tree.",
    "accounts_merge": "Merge accounts that share email addresses using union-find.",
    "number_of_provinces": "Count groups of directly or indirectly connected cities.",
    "longest_consecutive_sequence": "Find the length of the longest sequence of consecutive integers in an unsorted array.",
    # Intervals
    "merge_intervals": "Merge all overlapping intervals into non-overlapping ones.",
    "meeting_rooms": "Determine if a person can attend all meetings or find the minimum rooms needed.",
    "non_overlapping_intervals": "Find the minimum number of intervals to remove to make the rest non-overlapping.",
    # Dynamic Programming
    "coin_change": "Find the fewest coins needed to make a given amount, or determine it is impossible.",
    "house_robber": "Maximize the amount robbed from houses in a row without robbing two adjacent houses.",
    "word_break": "Determine if a string can be segmented into words from a given dictionary.",
    "edit_distance": "Find the minimum insertions, deletions, and substitutions to transform one string into another.",
    # Greedy
    "jump_game": "Determine whether you can reach the last index by jumping from each position.",
    "activity_selection": "Select the maximum number of non-overlapping activities from a set of start/end times.",
    "task_scheduler": "Find the minimum time to execute all tasks with a cooldown between identical tasks.",
    "gas_station": "Find the starting gas station that allows a complete circuit, or determine it is impossible.",
    # Backtracking
    "n_queens": "Place n queens on an n x n chessboard so no two queens threaten each other.",
    "permutations": "Generate all possible orderings of a collection of distinct elements.",
    "combinations": "Generate all ways to choose k elements from a set of n.",
    "subsets": "Generate all possible subsets of a given set of distinct elements.",
    "sudoku_solver": "Fill a 9x9 Sudoku grid so every row, column, and 3x3 box contains 1--9.",
    "word_search": "Determine if a word exists in a 2D grid by tracing adjacent cells.",
    # Bit Manipulation
    "single_number": "Find the element that appears only once when every other element appears twice.",
    "counting_bits": "For every number from 0 to n, count the number of 1-bits in its binary representation.",
    "reverse_bits": "Reverse the bit ordering of a 32-bit unsigned integer.",
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

    @classmethod
    def from_options(cls, opts: ExerciseOptions) -> ExercisePlan:
        return cls(
            root=opts["output_dir"],
            environment=opts["environment"],
            infrastructure=opts["infrastructure"],
            project_stage=opts["project_stage"],
            tasks=opts["tasks"],
            languages=opts["languages"],
            technologies=opts["technologies"],
            algorithms=opts["algorithms"],
            story=opts["story"],
        )

    def add_file(
        self,
        path: str | Path,
        description: str,
        content: str | None = None,
    ) -> FileSpec:
        spec = FileSpec(path=Path(path), description=description, content=content)
        self.files.append(spec)
        return spec
