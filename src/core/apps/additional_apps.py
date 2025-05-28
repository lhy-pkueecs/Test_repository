"""
This module defines applications below:
find, sort, uniq, cut, wc
which are concrete implementations of the App class.
"""

import os
import re
import fnmatch
from core.app import App
from core.app_factory import register
import sys


@register("find")
class Find(App):
    def _run(self, args):
        if len(args) < 2 or len(args) > 4:
            raise ValueError("wrong number of arguments.")

        if args[-2] != "-name":
            raise ValueError("Usage: find [PATH] -name PATTERN")

        pattern = args[-1]
        path_to_search = None

        if args[0] != "-name":
            path_to_search = args[0]
        else:
            path_to_search = "."

        # Validate the determined path_to_search
        if (
            not os.path.exists(path_to_search) or
            (not os.path.isdir(path_to_search))
        ):
            raise ValueError(f"Invalid path: {path_to_search}")

        for root, _, files in os.walk(path_to_search, followlinks=False):
            for filename in files:
                if fnmatch.fnmatch(filename, pattern):
                    print(os.path.join(root, filename))


@register("sort")
class Sort(App):
    def _run(self, args):
        if len(args) > 2:
            raise ValueError("wrong number of arguments")
        file = None
        option = None
        if len(args) == 1:
            if args[0] == "-r":
                option = args[0]
            else:
                file = args[0]
        elif len(args) == 2:
            option = args[0]
            file = args[1]
            if option != "-r":
                raise ValueError("Unknown option: " + option)
        if file is None:
            if sys.stdin.isatty():
                raise ValueError("empty input")
            else:
                file_lines = sys.stdin.readlines()
        else:
            with open(file, "r") as f:
                file_lines = f.readlines()
        sorted_lines = sorted(file_lines, reverse=(option == "-r"))
        for line in sorted_lines:
            print(line, end="")


@register("uniq")
class Uniq(App):
    def _run(self, args):
        if len(args) > 2:
            raise ValueError("wrong number of arguments")
        file = None
        option = None
        if len(args) == 1:
            if args[0] == "-i":
                option = args[0]
            else:
                file = args[0]
        elif len(args) == 2:
            option = args[0]
            file = args[1]
            if option != "-i":
                raise ValueError("Unknown option: " + option)
        if file is None:
            if sys.stdin.isatty():
                raise ValueError("empty input")
            else:
                file_lines = sys.stdin.readlines()
        else:
            with open(file, "r") as f:
                file_lines = f.readlines()
        unique_lines = [file_lines[0]]
        for i in range(1, len(file_lines)):
            line = file_lines[i]
            adjacent_line = file_lines[i-1]
            if option == "-i":
                if line.lower() != adjacent_line.lower():
                    unique_lines.append(line)
            else:
                if line != adjacent_line:
                    unique_lines.append(line)
        for line in unique_lines:
            print(line, end="")


@register("cut")
class Cut(App):
    def _run(self, args):
        if len(args) < 2 or len(args) > 3:
            raise ValueError("wrong number of arguments")
        if args[0] != "-b":
            raise ValueError("unknown option: " + args[0])
        extra_bytes = args[1]
        if len(args) == 3:
            file = args[2]
        else:
            file = None
        if file is None:
            if sys.stdin.isatty():
                raise ValueError("empty input")
            else:
                file_lines = sys.stdin.readlines()
        else:
            with open(file, "r") as f:
                file_lines = f.readlines()
        for line in file_lines:
            # Remove trailing newline character
            # add it back after processing
            line = line.rstrip('\n')
            try:
                result = self.__extract_bytes(line, extra_bytes)
                # Print the result with a newline
                print(result, end="\n")
            except ValueError as e:
                raise ValueError(f"Error specifying bytes: {e}") from e

    def __extract_bytes(self, line: str, bytes_spec: str) -> str:
        indices = set()
        line_len = len(line)
        try:
            parts = bytes_spec.split(',')
            for part in parts:
                part = part.strip()
                if not part:
                    # Skip empty parts resulting from command
                    # like ,, or trailing ,
                    continue

                # Case 1: N-M
                if '-' in part and part[0] != '-' and part[-1] != '-':
                    start_str, end_str = part.split('-', 1)
                    start = int(start_str)
                    end = int(end_str)
                    if start < 1 or end < start:
                        raise ValueError("invalid range")
                    # Convert to 0-based index range [start-1, end)
                    # Clamp indices to valid range for the line
                    py_start = max(0, start - 1)
                    py_end = min(line_len, end)
                    for i in range(py_start, py_end):
                        indices.add(i)

                # Case 2: N-
                elif part[-1] == '-' and part[:-1].isdigit():
                    start = int(part[:-1])
                    if start < 1:
                        raise ValueError("invalid range start")
                    # Convert to 0-based index range [start-1, line_len)
                    py_start = max(0, start - 1)
                    for i in range(py_start, line_len):
                        indices.add(i)

                # Case 3: -M
                elif part[0] == '-' and part[1:].isdigit():
                    end = int(part[1:])
                    if end < 1:
                        raise ValueError("invalid range end")
                    # Convert to 0-based index range [0, end)
                    py_end = min(line_len, end)
                    for i in range(0, py_end):
                        indices.add(i)

                # Case 4: N
                elif part.isdigit():
                    pos = int(part)
                    if pos < 1:
                        raise ValueError("invalid position")
                    # Convert to 0-based index
                    py_index = pos - 1
                    if 0 <= py_index < line_len:
                        indices.add(py_index)
                # Invalid format
                else:
                    raise ValueError(f"invalid byte/character specification: "
                                     f"{part}")
        except ValueError as e:
            # Re-raise with a more specific message if needed,
            # or handle differently
            raise ValueError(f"Error parsing byte/character specification "
                             f"'{bytes_spec}': {e}") from e
        # Sort indices and build the result string
        sorted_indices = sorted(list(indices))
        result = "".join(line[i] for i in sorted_indices)
        return result


@register("wc")
class Wc(App):
    def _run(self, args):
        if len(args) > 2:
            raise ValueError("wrong number of arguments")
        file = None
        option = None
        if len(args) == 0:
            option = "all"
        elif len(args) == 1:
            if args[0] in ["-l", "-w", "-m"]:
                option = args[0]
            else:
                option = "all"
                file = args[0]
        else:
            option = args[0]
            file = args[1]
            if option not in ["-l", "-w", "-m"]:
                raise ValueError("Unknown option: " + option)
        if file is None:
            if sys.stdin.isatty():
                raise ValueError("empty input")
            file_lines = sys.stdin.readlines()
        else:
            with open(file, "r") as f:
                file_lines = f.readlines()
        word_count = sum(len(re.findall(r'\S+', line.rstrip('\n')))
                         for line in file_lines)
        char_count = sum(len(line) for line in file_lines)
        if option == "-l":
            print(len(file_lines))
        elif option == "-w":
            print(word_count)
        elif option == "-m":
            print(char_count)
        else:
            print(len(file_lines))
            print(word_count)
            print(char_count)
