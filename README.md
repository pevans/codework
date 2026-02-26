# Codework

Codework is a tool that procedurally generates code exercises. You give it a
set of inputs that guide the generation of the exercise -- things like a
language you'd like to write in, a framework you want to use, and more.

## Installation

Codework makes use of `uv`. To install that locally, you can run the
following from the root of the codework repository:

```bash
uv tool install .
```

## Usage

Codework collects information about the type of exercise you want to generate
either directly from arguments or via an interactive prompt (`codework -i`).

Codework is designed to work in two stages. The first stage is to prepare a
spec file (named `SPEC.md`) in the provided exercise directory. This spec
fully describes the exercise to be implemented based on your choices.

The second stage is to implement the spec file. At the moment, this is not
handled by Codework; instead, you must direct an agent of your choosing to
implement the necessary accompanying files for the exercise. (Alternatively,
you can do all of that yourself as part of the exercise 😄)

The full usage text is below:

```
usage: codework [-h] [-i] [--environment {website,cli_app,http_service}]
                [--infrastructure {local,docker,cloud}]
                [--project-stage {greenfield,existing}] [--language LANGUAGE]
                [--technology TECHNOLOGY] [--algorithm ALGORITHM]
                [--tasks TASKS] [--dry-run]
                [output_dir]

Generate code exercises

positional arguments:
  output_dir            Directory to write the exercise files into

options:
  -h, --help            show this help message and exit
  -i, --interactive     Collect all options via interactive prompts
  --environment {website,cli_app,http_service}
                        Target environment for the exercise (required without
                        -i)
  --infrastructure {local,docker,cloud}
                        Infrastructure target for the exercise (required
                        without -i)
  --project-stage {greenfield,existing}
                        Project stage for the exercise (required without -i)
  --language LANGUAGE   Programming language for the exercise (required
                        without -i; may be repeated)
  --technology TECHNOLOGY
                        Framework or library used in the exercise (may be
                        repeated)
  --algorithm ALGORITHM
                        Algorithm to test with (may be repeated); choices:
                        two_sum, rotate_array,
                        longest_substring_without_repeating_characters,
                        product_of_array_except_self, group_anagrams,
                        subarray_sum_equals_k, lru_cache, three_sum,
                        container_with_most_water, trapping_rain_water,
                        min_window_substring, happy_number,
                        find_duplicate_number, reverse_a_linked_list,
                        merge_two_sorted_lists, detect_cycle,
                        copy_list_with_random_pointer, valid_parentheses,
                        daily_temperatures, largest_rectangle_in_histogram,
                        sliding_window_maximum,
                        search_in_rotated_sorted_array,
                        find_minimum_in_rotated_sorted_array,
                        koko_eating_bananas, ship_packages_in_d_days,
                        split_array_largest_sum, invert_binary_tree,
                        validate_bst, serialize_deserialize_binary_tree,
                        binary_tree_maximum_path_sum, level_order_traversal,
                        path_sum, diameter_of_binary_tree,
                        kth_largest_element, merge_k_sorted_lists,
                        find_median_from_data_stream, implement_trie,
                        word_search_ii, design_search_autocomplete,
                        breadth_first_search, depth_first_search,
                        number_of_islands, clone_graph, course_schedule,
                        network_delay_time, topological_sort,
                        alien_dictionary, number_of_connected_components,
                        redundant_connection, accounts_merge,
                        number_of_provinces, longest_consecutive_sequence,
                        merge_intervals, meeting_rooms,
                        non_overlapping_intervals, coin_change, house_robber,
                        word_break, edit_distance, jump_game,
                        activity_selection, task_scheduler, gas_station,
                        n_queens, permutations, combinations, subsets,
                        sudoku_solver, word_search, single_number,
                        counting_bits, reverse_bits
  --tasks TASKS         Number of tasks in the exercise (required without -i)
  --dry-run             Print what would be written without touching the
                        filesystem
```

## General configuration

Codework allows you to configure a number of parameters for the exercise:

- Number of tasks to be completed (more tasks = more time necessary)
- Type of system to build (a website; a CLI application; an HTTP service)
- Project stage (greenfield: you build everything from scratch; existing
  project, you modify some existing code base)
- Languages to use for implementation
- Technologies to use (frameworks, libraries, and so forth)
- Where the solution is hosted (all local to the machine; in docker; in a
  cloud provider)

## Algorithms

Codework can also use any number of algorithms as goals for the exercise it
generates. It focuses on the following categories:

- Arrays & Hashing
- Backtracking
- Binary Search
- Bit Manipulation
- Dynamic Programming
- Graphs
- Greedy
- Heaps
- Intervals
- Linked Lists
- Stacks & Queues
- Trees
- Tries
- Two Pointers & Sliding Window
- Union-Find

## Contributing

This repository is not accepting outside contributions at this time.

## License

MIT.
